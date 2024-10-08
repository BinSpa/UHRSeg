# dataset settings
dataset_type = 'GIDDataset'
data_root = '/data1/gyl/RS_DATASET/FBP'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
crop_size = (2500, 2500)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations'),
    dict(type='Resize', scale=(5000, 5000)),
    dict(type='RandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='RandomFlip', prob=0.5),
    dict(type='RandomRotate', prob=0.5, degree=(90, 270)),
    dict(type='PhotoMetricDistortion'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size=crop_size, pad_val=0, seg_pad_val=255),
    # dict(type='DefaultFormatBundle'),
    dict(type='PackSegInputs'),
    # dict(type='Collect', keys=['img', 'gt_semantic_seg']),
    dict(type='Collect', keys=['img', 'gt_seg_map']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(5000, 5000),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='ImageToTensor', keys=['img', 'gt_seg_map']),
            dict(type='Collect', keys=['img', 'get_seg_map']),
        ])
]

train_dataloader = dict(
    batch_size=1,
    num_workers=10,
    persistent_workers=True,
    sampler=dict(type='InfiniteSampler', shuffle=True),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        data_prefix=dict(
            img_path='train/rgb_images', seg_map_path='train/gid_labels'),
        pipeline=train_pipeline))
val_dataloader = dict(
    batch_size=1,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        data_prefix=dict(
            img_path='val/rgb_images', seg_map_path='val/gid_labels'),
        pipeline=test_pipeline))

test_dataloader = val_dataloader

val_evaluator = dict(type='IoUMetric', iou_metrics=['mIoU'])
test_evaluator = val_evaluator

'''
data = dict(
    samples_per_gpu=16,
    workers_per_gpu=10,
    train=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='img_dir/train',
        ann_dir='rgb2id/train',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='img_dir/val',
        ann_dir='rgb2id/val',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='img_dir/test',
        ann_dir='rgb2id/test',
        pipeline=test_pipeline))
'''