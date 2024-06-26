# Copyright (c) OpenMMLab. All rights reserved.
import torch
import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import ConvModule

from mmseg.models.decode_heads.decode_head import BaseMultiCropDecodeHead

from mmseg.registry import MODELS
from ..utils import resize

from .replknet import RepLKNetStage


class ConvMLP(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(ConvMLP, self).__init__()
        # 第一层1x1卷积，相当于MLP的隐藏层
        self.conv1 = nn.Conv2d(in_channels, hidden_channels, kernel_size=1)
        # 第二层1x1卷积，相当于MLP的输出层
        self.conv2 = nn.Conv2d(hidden_channels, out_channels, kernel_size=1)

    def forward(self, x):
        x = F.relu(self.conv1(x))  # 激活函数可以根据需要替换
        x = self.conv2(x)
        return x


@MODELS.register_module()
class Proto_SegformerHead(BaseMultiCropDecodeHead):
    """The all mlp Head of segformer.

    This head is the implementation of
    `Segformer <https://arxiv.org/abs/2105.15203>` _.

    Args:
        interpolate_mode: The interpolate mode of MLP head upsample operation.
            Default: 'bilinear'.
    """

    def __init__(self, k=10, momentum=0.999, text_path=None, interpolate_mode='bilinear', 
                 iflk=False, large_kernel_sizes=[31,29,27,13], layers=[2,2,2,2], drop_path_rate=0.3,
                 small_kernel=5, dw_ratio=1, ffn_ratio=4, small_kernel_merged=False, norm_intermediate_features=False,
                 **kwargs):
        super().__init__(input_transform='multiple_select', **kwargs)

        self.interpolate_mode = interpolate_mode
        num_inputs = len(self.in_channels)

        assert num_inputs == len(self.in_index)

        self.convs = nn.ModuleList()
        for i in range(num_inputs):
            self.convs.append(
                ConvModule(
                    in_channels=self.in_channels[i],
                    out_channels=self.channels,
                    kernel_size=1,
                    stride=1,
                    norm_cfg=self.norm_cfg,
                    act_cfg=self.act_cfg))
        # convmodule for fusion all feature 
        self.fusion_conv = ConvModule(
            in_channels=self.channels * num_inputs + 54 + 64,
            out_channels=self.channels,
            kernel_size=1,
            norm_cfg=self.norm_cfg)
        # text feature for prototype
        text_feature = torch.load(text_path, map_location='cpu')
        self.prototypes = nn.Parameter(text_feature,
                                       requires_grad=False)
        self.k = k
        self.momentum = momentum
        # MLP to align image feature to text feature
        self.img_project = ConvMLP(in_channels=self.channels * num_inputs, hidden_channels=1024, out_channels=1024)
        # large kernel to extract feature
        self.iflk = iflk
        if self.iflk:
            # conv module
            self.lk_stages = nn.ModuleList()
            dpr = [x.item() for x in torch.linspace(0, drop_path_rate, sum(layers))]
            for stage_idx in range(num_inputs):
                lk_layer = RepLKNetStage(channels=self.in_channels[stage_idx], num_blocks=layers[stage_idx],
                        stage_lk_size=large_kernel_sizes[stage_idx],
                        drop_path=dpr[sum(layers[:stage_idx]):sum(layers[:stage_idx + 1])],
                        small_kernel=small_kernel, dw_ratio=dw_ratio, ffn_ratio=ffn_ratio,
                        use_checkpoint=False, small_kernel_merged=small_kernel_merged,
                        norm_intermediate_features=norm_intermediate_features)
                self.lk_stages.append(lk_layer)
            # fusion module
            self.lk_convs = ConvModule(
                    in_channels=1024,
                    out_channels=64,
                    kernel_size=1,
                    stride=1,
                    norm_cfg=self.norm_cfg,
                    act_cfg=self.act_cfg)


    def forward(self, inputs):
        # Receive 4 stage backbone feature map: 1/4, 1/8, 1/16, 1/32
        # large kernel handle
        lk_outs = []
        if self.iflk:
            for idx, input in enumerate(inputs):
                lk_outs.append(self.lk_stages[idx](input))
            for idx, lk_out in enumerate(lk_outs):
                lk_outs[idx] = resize(input=lk_out,
                                      size=lk_outs[0].shape[2:],
                                      mode=self.interpolate_mode,
                                      align_corners=self.align_corners)
            lk_features = self.lk_convs(torch.cat(lk_outs, dim=1))
        inputs = self._transform_inputs(inputs)
        outs = []
        for idx in range(len(inputs)):
            x = inputs[idx]
            conv = self.convs[idx]
            outs.append(
                resize(
                    input=conv(x),
                    size=inputs[0].shape[2:],
                    mode=self.interpolate_mode,
                    align_corners=self.align_corners))

        outs_feature = torch.cat(outs, dim=1)
        project_outs = self.img_project(outs_feature)
        # normalize
        norm_outs = project_outs / project_outs.norm(dim=1, keepdim=True)
        norm_protos = self.prototypes / self.prototypes.norm(dim=1, keepdim=True)
        # cosine similarity
        similarity_map = torch.einsum('nd,bdhw->bnhw', norm_protos, norm_outs)
        # generate mask using entropy
        entropy_imgtxt_feature = F.softmax(similarity_map, dim=1)
        entropies = -(entropy_imgtxt_feature * entropy_imgtxt_feature.clamp(min=1e-12).log2()).sum(dim=1)
        entropy_mask = (entropies > 5.75476).float()
        # assert False, "lk_features:{}; entropy_mask:{}".format(lk_features.shape, entropy_mask.shape)
        lk_features = lk_features * (entropy_mask.unsqueeze(1))
        # select pixels to update prototypes
        n, d = norm_protos.shape
        b, _, h, w  = norm_outs.shape
        
        new_prototypes = self.prototypes.clone()
        for i in range(n):
            similarity_map_i = similarity_map[:, i, :, :]
            # find topk similarity
            topk_values, topk_indices = torch.topk(similarity_map_i.view(b, -1), k=self.k, dim=1, largest=True, sorted=False)
            # (b,k) -> (b,d,k)
            topk_indices = topk_indices.unsqueeze(1).expand(-1, d, -1)
            project_outs_flat = project_outs.view(b, d, h*w)
            # (b, d, 10)
            topk_feature_vectors = torch.gather(project_outs_flat, 2, topk_indices)
            # mean:(b,d)
            topk_feature_vectors = topk_feature_vectors.mean(dim=2)
            # calculate all batch means:(d,)
            mean_feature_vector = topk_feature_vectors.mean(dim=0)
            # momentum
            assert self.prototypes[i].shape == mean_feature_vector.shape, "prototypes:{}, mean_feature_vector:{}".format(self.prototypes[i].shape, mean_feature_vector.shape)
            new_prototypes[i] = self.momentum * self.prototypes[i] + (1 - self.momentum) * mean_feature_vector
        self.prototypes.data.copy_(new_prototypes)
        # fusion feautres
        outs.append(similarity_map)
        outs.append(lk_features)
        out = self.fusion_conv(torch.cat(outs, dim=1))

        out = self.cls_seg(out)

        return out
    
    def _stack_batch_gt(self, batch_data_samples):
        if 'mc_seg_map' in batch_data_samples[0]:
            gt_semantic_segs = [
                data_sample.mc_seg_map.data for data_sample in batch_data_samples
            ]
        else:
            gt_semantic_segs = [
                data_sample.gt_sem_seg.data for data_sample in batch_data_samples
            ]
        gt_semantic_segs = torch.stack(gt_semantic_segs, dim=0)
        assert len(gt_semantic_segs.shape) == 4, "gt shape is {}".format(gt_semantic_segs.shape)
        b, m, h, w = gt_semantic_segs.shape
        gt_semantic_segs = gt_semantic_segs.reshape(b*m, h, w)
        return gt_semantic_segs.unsqueeze(1)
