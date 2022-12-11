# -*- coding: utf-8 -*-
# @Time    : 2022/8/23 9:49
# @Author  : HongFei Wang
import torch
from model import UNet
from ulits import Units
from torch.utils.data import DataLoader
from torchvision.transforms import transforms
from data import Datasets
import warnings
warnings.filterwarnings('ignore')
hyper_parameter = {
    'lr': 1e-4,  # 学习率
    'weight_decay': 5e-4,  # 权重衰减
    'epoch': 20,  # 训练次数
    'pth_path': '',  # 预训练权重 不使用则空就行
    'data_root': './datas',  # 数据路径   image-label
    'mean_std_count': False,
    'num_workers': 0,
    'batch_size': 8,
}

transform = {
    'tfs_train': transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=torch.tensor([0.2949071, 0.30734208, 0.34141582]),
                             std=torch.tensor([0.25307885, 0.23292585, 0.21397737])),
    ]),
    'tfs_test': transforms.Compose([
        transforms.ToTensor(),
    ])
}

model = UNet()
train_data = Datasets(train=True,
                      root=hyper_parameter['data_root'],
                      tfs=transform['tfs_train'])
test_data = Datasets(train=True,
                     root=hyper_parameter['data_root'],
                     tfs=transform['tfs_test'])
train_loader = DataLoader(dataset=train_data,
                          batch_size=hyper_parameter['batch_size'],
                          shuffle=True,
                          num_workers=hyper_parameter['num_workers'],
                          pin_memory=True)
test_loader = DataLoader(dataset=test_data,
                         batch_size=hyper_parameter['batch_size'],
                         shuffle=False,
                         num_workers=hyper_parameter['num_workers'],
                         pin_memory=True)

mains = Units(net=model,
              net_name='unet',
              EPOCH=hyper_parameter['epoch'],
              train_data=train_loader,
              test_data=test_loader,
              optimer='adamw',
              scheduler='MUL',
              best=0, mdl_path=None,
              lr=hyper_parameter['lr'],
              milestones=[250, 300],
              gamma=0.1,
              weight_decay=5e-4)

if __name__ == '__main__':
    if hyper_parameter['mean_std_count']:
        mains.mean_std()
    else:
        mains.run()
