# mc_text
bash torchrun_test.sh ../configs/mctextnet/segformer_urur.py ../../mmseg_exp/mctxt_urur/iter_112000.pth 1 --work-dir ../../mmseg_exp/mctxt_urur
bash torchrun_test.sh ../configs/mctextnet/segformer_gid.py ../../mmseg_exp/mctxt_gid/iter_96000.pth 1 --work-dir ../../mmseg_exp/mctxt_gid
# baseline
bash torchrun_test.sh ../configs/segformer/segformer-b5_fbp.py /home/rsr/gyl/RS_Code/Paper_Graph/Introduction/segformer_ckpts/fbp.pth 1 --work-dir ../../mmseg_exp/segformerb5_fbp
bash torchrun_test.sh ../configs/segformer/segformer_mit-b5_8xb2-160k_gid-512x512.py /home/rsr/gyl/RS_Code/Paper_Graph/Introduction/segformer_ckpts/mc_gid.pth 1 --work-dir ../../mmseg_exp/segformerb5_gid