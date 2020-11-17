import cv2
import os
from matplotlib import pyplot as plt
import numpy as np

images = []

path = ['pics/cut_all/healthy', 'pics/cut_all/COVID-19']
imgList_h = os.listdir(path[0])
imgList_c = os.listdir(path[1])

for i in imgList_h:
    imgCurr = cv2.imread(f'{path[0]}/{i}', 0)
    images.append(imgCurr)
for i in imgList_c:
    imgCurr = cv2.imread(f'{path[1]}/{i}', 0)
    images.append(imgCurr)

imgList_merge = imgList_h + imgList_c

plot = True

for i in range(0, len(images)):
    # podziel na pół histogram i prównaj energie
    img = images[i]
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # img = clahe.apply(img)
    h = [(img == v).sum() for v in range(256)]
    h = np.array(h)
    norm_h = h/h.sum()

    cumul_h = np.zeros((256,))
    for j in range(256):
        cumul_h[j] = norm_h[j] + cumul_h[j-1]

    if plot is True:
        plt.subplot(121)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)
        plt.title(os.path.splitext(imgList_merge[i])[0].replace('_', ' '))
        plt.subplot(122)
        plt.bar(range(256), cumul_h)
        # plt.hist(img.ravel(), 256, [0, 256])
        plt.show()


