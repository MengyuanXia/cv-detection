_base_ = [
    '../_base_/schedules/schedule_1x.py',
    '../_base_/default_runtime.py'
    # '../_base_/datasets/voc0712.py'
]


data_preprocessor = dict(
    type='DetDataPreprocessor',
    mean=[0, 0, 0],
    std=[255., 255., 255.],
    bgr_to_rgb=True,
    pad_size_divisor=32
)

model = dict(
    type='YOLOV3',
    data_preprocessor=data_preprocessor,
    backbone=dict(
        type='Darknet',
        depth=53,
        out_indices=(3, 4, 5),
        init_cfg=dict(type='Pretrained', checkpoint='open-mmlab://darknet53')
    ),
    neck=dict(
        type='YOLOV3Neck',
        num_scales=3,
        in_channels=[1024, 512, 256],
        out_channels=[512, 256, 128]
    ),
    bbox_head=dict(
        type='YOLOV3Head',
        num_classes=20,
        in_channels=[512, 256, 128],
        out_channels=[1024, 512, 256],
        anchor_generator=dict(
            type='YOLOAnchorGenerator',
            base_sizes=[[(116, 90), (156, 198), (373, 326)],
                        [(30, 61), (62, 45), (59, 119)],
                        [(10, 13), (16, 30), (33, 23)]],
            strides=[32, 16, 8]
        ),
        bbox_coder=dict(type='YOLOBBoxCoder'),
        featmap_strides=[32, 16, 8],
        loss_cls=dict(
            type='CrossEntropyLoss',
            use_sigmoid=True,
            loss_weight=1.0,
            reduction='sum'
        ),
        loss_conf=dict(
            type='CrossEntropyLoss',
            use_sigmoid=True,
            loss_weight=1.0,
            reduction='sum'
        ),
        loss_xy=dict(
            type='CrossEntropyLoss',
            use_sigmoid=True,
            loss_weight=2.0,
            reduction='sum'
        ),
        loss_wh=dict(type='MSELoss', loss_weight=2.0, reduction='sum')
    ),
    train_cfg=dict(
        assigner=dict(
            type='GridAssigner',
            pos_iou_thr=0.5,
            neg_iou_thr=0.5,
            min_pos_iou=0
        )
    ),
    test_cfg=dict(
        nms_pre=1000,
        min_bbox_size=0,
        score_thr=0.05,
        conf_thr=0.005,
        nms=dict(type='nms', iou_threshold=0.45),
        max_per_img=100
    )
)


dataset_type = 'VOCDataset'
data_root = 'data/VOCdevkit/'

backend_args = None

train_pipeline = [
    dict(type='LoadImageFromFile', backend_args=backend_args),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', scale=(1000, 600), keep_ratio=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PackDetInputs')
]

test_pipeline = [
    dict(type='LoadImageFromFile', backend_args=backend_args),
    dict(type='Resize', scale=(1000, 600), keep_ratio=True),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape', 'scale_factor')
    )
]

train_dataloader = dict(
    batch_size=8,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    batch_sampler=dict(type='AspectRatioBatchSampler'),
    dataset=dict(
        type='RepeatDataset',
        times=3,
        dataset=dict(
            type='ConcatDataset',
            datasets=[
                dict(
                    type=dataset_type,
                    data_root=data_root,
                    ann_file='VOC2007/ImageSets/Main/trainval.txt',
                    data_prefix=dict(sub_data_root='VOC2007/'),
                    filter_cfg=dict(filter_empty_gt=True, min_size=32, bbox_min_size=32),
                    pipeline=train_pipeline,
                    backend_args=backend_args
                ),
                dict(
                    type=dataset_type,
                    data_root=data_root,
                    ann_file='VOC2012/ImageSets/Main/trainval.txt',
                    data_prefix=dict(sub_data_root='VOC2012/'),
                    filter_cfg=dict(filter_empty_gt=True, min_size=32, bbox_min_size=32),
                    pipeline=train_pipeline,
                    backend_args=backend_args
                )
            ]
        )
    )
)

val_dataloader = dict(
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='VOC2007test/ImageSets/Main/test.txt',
        data_prefix=dict(sub_data_root='VOC2007test/'),
        test_mode=True,
        pipeline=test_pipeline,
        backend_args=backend_args
    )
)

test_dataloader = val_dataloader

val_evaluator = dict(type='VOCMetric', metric='mAP', eval_mode='11points')
test_evaluator = val_evaluator

train_cfg = dict(max_epochs=15, val_interval=3)

optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(type='SGD', lr=0.001, momentum=0.9, weight_decay=0.0005),
    clip_grad=dict(max_norm=35, norm_type=2)
)

param_scheduler = [
    dict(type='LinearLR', start_factor=0.1, by_epoch=False, begin=0, end=2000),
    dict(type='MultiStepLR', by_epoch=True, milestones=[218, 246], gamma=0.1)
]

default_hooks = dict(checkpoint=dict(type='CheckpointHook', interval=3))

auto_scale_lr = dict(base_batch_size=64)

log_config = dict(
    interval=3,
    hooks=[
        dict(type='TextLoggerHook'),
        dict(type='TensorboardLoggerHook')
    ])
#work_dir = './work_dirs/yolov3_voc_experiment'