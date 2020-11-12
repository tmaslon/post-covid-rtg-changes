# Not working; Bad approach

import cv2
import os
from matplotlib import pyplot as plt

path = 'pics/healthy'
img_ref = cv2.imread('pics/ref_image.jpg')
imgList = os.listdir(path)
images = []

for i in imgList:
    imgCurr = cv2.imread(f'{path}/{i}', 0)
    images.append(imgCurr)

for i in images:
    trans = cv2.GaussianBlur(i, (5,5), 0)
    # trans = cv2.Laplacian(i, cv2.CV_64F)
    plt.imshow(trans, cmap='gray')
    plt.show()

    _, thresh = cv2.threshold(trans, 20, 255, cv2.THRESH_BINARY)
    plt.imshow(thresh, cmap='gray')
    plt.show()

    dilated = cv2.dilate(thresh, None, iterations=3)
    plt.imshow(dilated)
    plt.show()

    countours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    (x, y, w, h) = cv2.boundingRect(countours)
    crop_img = i[y:y+h, x:x+w]
    plt.imshow(crop_img, cmap='gray')
