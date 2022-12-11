# -*- coding: utf-8 -*-
# @Time    : 2022/8/23 9:38
# @Author  : HongFei Wang
from torch import nn
import torch
class UpSampleLayer(nn.Module):
    def __init__(self,in_ch,out_ch):
        # 512-1024-512
        # 1024-512-256
        # 512-256-128
        # 256-128-64
        super(UpSampleLayer, self).__init__()
        self.Conv_BN_ReLU_2 = nn.Sequential(
            nn.Conv2d(in_channels=in_ch, out_channels=out_ch*2, kernel_size=3, stride=1,padding=1),
            nn.BatchNorm2d(out_ch*2),
            nn.ReLU(),
            nn.Conv2d(in_channels=out_ch*2, out_channels=out_ch*2, kernel_size=3, stride=1,padding=1),
            nn.BatchNorm2d(out_ch*2),
            nn.ReLU()
        )
        self.upsample=nn.Sequential(
            # pad = k//2
            # down -->s==2-->下采样2倍  -->上采样2倍-->图像扩大2倍
            nn.ConvTranspose2d(in_channels=out_ch*2,
                               out_channels=out_ch,
                               kernel_size=3,
                               stride=2,
                               padding=1,
                               output_padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU()
        )
        # 1 3
        # 5 7
        # 2，2 --> 2,3  1 2 3   5 6 7
    def forward(self,x,out):
        '''
        :param x: 输入卷积层
        :param out:与上采样层进行cat
        :return:
        '''
        x_out=self.Conv_BN_ReLU_2(x)

        # 尝试自己加
        x_out=self.upsample(x_out)
        #  B C W H  沿着C 拼接---> C c1+c2
        cat_out=torch.cat((x_out,out),dim=1)
        return cat_out
