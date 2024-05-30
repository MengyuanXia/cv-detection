# Yolo v3

### 数据准备

```bash
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCdevkit_08-Jun-2007.tar
```

### 训练模型
```bash
bash tools/dist_train.sh ./configs/yolo/yolov3_d53_8xb8-ms-608-273e_voc.py 8
```
### 测试模型
```bash
bash tools/dist_test.sh configs/yolo/yolov3_d53_8xb8-ms-608-273e_voc.py work_dirs/yolov3_d53_8xb8-ms-608-273e_voc/yolov3_d53.pth 8
```

### 模型结果可视化
```bash
tensorboard --logdir={vis_log_dir} --port=6006
```
### 模型权重
https://pan.baidu.com/s/1FuPfj7OJIZDKTTU3_JLUdA?pwd=4321
