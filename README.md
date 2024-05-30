# Yolo v3

### 数据准备
下载数据

```bash
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCdevkit_08-Jun-2007.tar
```
2.修改configs/base/datasets/voc0712.py 里的数据路径


### 训练模型
config_file = "./configs/regnet/faster-rcnn_regnetx-3.2GF_fpn_ms-3x_coco.py"
log_dir = "/path/to/logdir"  # 修改为保存日志的路径

### 修改默认的日志保存地址
runtime_config_file = "./configs/base/default_runtime.py"
with open(runtime_config_file, "r") as f:
    runtime_config_data = f.read()

new_runtime_config_data = runtime_config_data.replace("/your/path/to/logdir", log_dir)

with open(runtime_config_file, "w") as f:
    f.write(new_runtime_config_data)

### 训练模型
train_command = f"python tools/train.py {config_file}"
subprocess.run(train_command, shell=True)

### 模型结果可视化
vis_log_dir = "/path/to/vis-result"  # 修改为可视化日志保存的路径
tensorboard_command = f"tensorboard --logdir={vis_log_dir} --port=6006"
subprocess.run(tensorboard_command, shell=True)
