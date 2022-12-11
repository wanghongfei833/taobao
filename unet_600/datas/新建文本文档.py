import matplotlib.pyplot as plt

img1 = r'E:\taobao\unet_600\datas\image\123455_07.jpg'
img2 = r'E:\taobao\unet_600\datas\label\01_07.jpg'
plt.figure()
img1 = plt.imread(img1)
plt.imshow(img1)
plt.figure()
img2 = plt.imread(img2)
plt.imshow(img2[:,:,0],cmap='gray')
plt.show()
