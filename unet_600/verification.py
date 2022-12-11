# -*- coding: utf-8 -*-
# @Time    : 2022/8/25 10:50
# @Author  : HongFei Wang
import numpy as np
from torch.nn import functional as F
from model import UNet
import matplotlib.pyplot as plt
import torch
from torchvision import transforms
from PIL import Image
image_path = r'E:\taobao\unet_600\datas\image\123455_06.jpg'
label_path = r'E:\taobao\unet_600\datas\label\01_06.jpg'
model_path = './Mdl_Data/unet/4.pth'

def pads(image,label,size,mean_std=None):
    crop = transforms.RandomCrop(size)

    if mean_std:
        trans_image = transforms.Compose([transforms.ToTensor(),
                                      transforms.Normalize(mean_std[0],mean_std[1])
                                      ])
    else:
        trans_image = transforms.Compose([transforms.ToTensor()])
    trans_label = transforms.Compose([transforms.ToTensor()])
    image = trans_image(image)
    label = trans_label(label)
    x_pad = size - image.shape(1)
    y_pad = size - label.shape(2)
    image = F.pad(image,(0,y_pad,0,x_pad,0,0))
    label = F.pad(label,(0,y_pad,0,x_pad,0,0))
    seed = torch.random.seed()
    torch.random.manual_seed(seed)
    image = crop(image)
    torch.random.manual_seed(seed)
    label = crop(label)
    return image,label
model = UNet()
size = 512
# model.load_state_dict(torch.load(model_path))
# image_data = Image.open(image_path)
# label      = Image.open(label_path)
image= Image.fromarray(np.ones((128,512,3),np.uint8))
label = Image.fromarray(np.zeros((128,512),np.uint8))

image,label = pads(image,label,256,None)
label = label[0].numpy()
image_data = image.permute(1,2,0).numpy()
image = image.unsqueeze(0)


with torch.no_grad():
    image = model(image)
    image = torch.argmax(image,dim=1)
image = image.squeeze().detach().numpy()

plt.subplot(121)
plt.imshow(image_data)
plt.imshow(label,alpha=0.5)

plt.subplot(122)
plt.title('output')
plt.imshow(image_data)
plt.imshow(image,alpha=0.5)

plt.show()
