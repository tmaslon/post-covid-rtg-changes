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
    pass