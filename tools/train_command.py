bash torchrun_train.sh /mnt/data/nas/gyl/RS_Code/mmsegmentation/configs/pvtv2/pvtv2-b5_blu-512x512.py 2 --work-dir /mnt/data/nas/gyl/RS_Code/mmsegmentation/experiments/pvtv2_blu
bash torchrun_train.sh /data/RS_Code/mmsegmentation/configs/deeplabv3plus/deeplabv3plus_r101-80k_blu-512x512.py 2 --work-dir /data/RS_Code/mmsegmentation/experiments/deeplabv3p_blu
bash torchrun_train.sh ../configs/segformer/segformer-b2_gid.py 1 --work-dir ../../mmseg_exp/segformerb2_gid
bash torchrun_train.sh ../configs/segformer/segformer-b5_fbp.py 2 --work-dir ../../mmseg_exp/segformerb5_fbp
# deeplabv3+
bash torchrun_train.sh /mnt/data/nas/gyl/RS_Code/mmsegmentation/configs/deeplabv3plus/deeplabv3plus_r101-d8_4xb4-160k_gid-512x512.py 1 --work-dir /mnt/data/nas/gyl/RS_Code/mmseg_exp/deeplab_gid
bash torchrun_train.sh /mnt/data/nas/gyl/RS_Code/mmsegmentation/configs/segformer/segformer_mit-b5_8xb2-160k_gid-512x512.py 1 --work-dir /mnt/data/nas/gyl/RS_Code/mmseg_exp/segformer_gid
bash torchrun_train.sh /mnt/data/nas/gyl/RS_Code/mmsegmentation/configs/segformer/segformer_mit-b5_8xb2-160k_urur-512x512.py 1 --work-dir /mnt/data/nas/gyl/RS_Code/mmseg_exp/segformer_urur
bash torchrun_train.sh /mnt/data/nas/gyl/RS_Code/mmsegmentation/configs/deeplabv3plus/deeplabv3plus_r101-d8_4xb4-160k_urur-512x512.py 1 --work-dir /mnt/data/nas/gyl/RS_Code/mmseg_exp/deeplab_urur
bash torchrun_train.sh ../configs/deeplabv3plus/deeplabv3plus_r101-d8_4xb4-160k_fbp-512x512.py 2 --work-dir ../../mmseg_exp/deeplabv3p_fbp
# swin-base
bash torchrun_train.sh ../configs/swin/swin-base-patch4-window7-fbp-512x512.py 2 --work-dir ../../mmseg_exp/swinbase_fbp
bash torchrun_train.sh ../configs/swin/swin-base-patch4-window7-urur-512x512.py 2 --work-dir ../../mmseg_exp/swinbase_urur
bash torchrun_train.sh ../configs/swin/swin-base-patch4-window7-gid-512x512.py 2 --work-dir ../../mmseg_exp/swinbase_gid
# mc exp
bash torchrun_train.sh ../configs/multicropnet/segformer_mit-b5_8xb2-160k_gid-512x512-ce.py 1 --work-dir /data9/gyl/RS_Code/mmseg_exp/mcgid_ce
bash torchrun_train.sh ../configs/multicropnet/segformer_mit-b5_8xb2-160k_urur-512x512-ce.py 1 --work-dir /data9/gyl/RS_Code/mmseg_exp/mcurur_ce
bash torchrun_train.sh ../configs/multicropnet/segformer-b5_fbp.py 2 --work-dir ../../mmseg_exp/mc_fbp
# mccolor
bash torchrun_train.sh ../configs/multicropnet/segformer_mit-b5_8xb2-160k_gid-512x512-ce.py 1 --work-dir /data9/gyl/RS_Code/mmseg_exp/mcgid_color
bash torchrun_train.sh ../configs/multicropnet/segformer_mit-b5_8xb2-160k_urur-512x512-ce.py 1 --work-dir /data9/gyl/RS_Code/mmseg_exp/mcurur_color
# mctext exp
bash torchrun_train.sh ../configs/mctextnet/segformer_gid.py 2 --work-dir ../../mmseg_exp/mctext_gid
bash torchrun_train.sh ../configs/mctextnet/segformer_urur.py 2 --work-dir ../../mmseg_exp/mctext_urur
bash torchrun_train.sh ../configs/mctextnet/segformer_fbp.py 2 --work-dir ../../mmseg_exp/mctext_fbp
# proto exp
bash torchrun_train.sh ../configs/mctextnet/segformer-b2_gid_proto.py 1 --work-dir ../../mmseg_exp/proto_gid
bash torchrun_train.sh ../configs/mctextnet/segformer-b2_urur_proto.py 1 --work-dir ../../mmseg_exp/proto_urur
bash torchrun_train.sh ../configs/mctextnet/segformer-b2_gid_proto_lk.py 1 --work-dir ../../mmseg_exp/proto_lk_gid
bash torchrun_train.sh ../configs/mctextnet/segformer-b2_urur_proto_lk.py 1 --work-dir ../../mmseg_exp/proto_lk_urur
# mcfusion exp
bash torchrun_train.sh /mnt/data/nas/gyl/RS_Code/mmsegmentation/configs/mcfusionnet/segformer_mit-b5_8xb2-160k_gid-512x512.py 1 --work-dir /mnt/data/nas/gyl/RS_Code/mmseg_exp/mcfusion_gid
bash torchrun_train.sh /mnt/data/nas/gyl/RS_Code/mmsegmentation/configs/mcfusionnet/segformer_mit-b5_8xb2-160k_urur-512x512.py 1 --work-dir /mnt/data/nas/gyl/RS_Code/mmseg_exp/mcfusion_urur
bash torchrun_train.sh /home/rsr/gyl/RS_Code/mmsegmentation/configs/mcfusionnet/segformer_mit-b5_8xb2-160k_gid-512x512_onlyfusion.py 1 --work-dir /home/rsr/gyl/RS_Code/mmseg_exp/onlyfusion_gid
# onlyfusion
bash torchrun_train.sh /data9/gyl/RS_Code/mmsegmentation/configs/onlyfusion/segformer_mit-b5_8xb2-160k_gid-512x512_onlyfusion.py 1 --work-dir /data9/gyl/RS_Code/mmseg_exp/segformer_gid_onlyfusion
bash torchrun_train.sh /data9/gyl/RS_Code/mmsegmentation/configs/onlyfusion/segformer_mit-b5_8xb2-160k_urur-512x512_onlyfusion.py 1 --work-dir /data9/gyl/RS_Code/mmseg_exp/segformer_urur_onlyfusion
# sam 
bash torchrun_train.sh ../configs/samhqnet/segformer_gid.py 1 --work-dir /data1/gyl/RS_Code/mmseg_exp/samhq_gid
bash torchrun_train.sh ../configs/samhqnet/segformer_urur.py 1 --work-dir /data1/gyl/RS_Code/mmseg_exp/samhq_urur
bash torchrun_train.sh ../configs/samhqnet/segformer_fbp.py 1 --work-dir /data1/gyl/RS_Code/mmseg_exp/samhq1_fbp
# only sam
bash torchrun_train.sh ../configs/samhqnet/segformer_onlysam_gid.py 2 --work-dir /data1/gyl/RS_Code/mmseg_exp/onlysam_gid
bash torchrun_train.sh ../configs/samhqnet/segformer_onlysam_fbp.py 2 --work-dir /data1/gyl/RS_Code/mmseg_exp/onlysam_fbp
bash torchrun_train.sh ../configs/samhqnet/segformer_onlysam_urur.py 2 --work-dir /data1/gyl/RS_Code/mmseg_exp/onlysam_urur
# unet 
bash torchrun_train.sh ../configs/unet/unet_s5-d16_fcn_4xb4-160k_gid.py 1 --work-dir /data1/gyl/RS_Code/mmseg_exp/unet_gid
bash torchrun_train.sh ../configs/unet/unet_s5-d16_fcn_4xb4-160k_urur.py 1 --work-dir /data1/gyl/RS_Code/mmseg_exp/unet_urur
bash torchrun_train.sh ../configs/unet/unet_s5-d16_fcn_4xb4-160k_fbp.py 1 --work-dir /data1/gyl/RS_Code/mmseg_exp/unet_fbp