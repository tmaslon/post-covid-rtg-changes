# Not working; Bad approach

import cv2
import os
from matplotlib import pyplot as plt
import numpy as np

path = 'pics/healthy'
img_ref = cv2.imread('pics/ref_image.jpg', 0)
imgList = os.listdir(path)
images = []
images_new = cv2.imread('pics/COVID-19/covid19_30yo_female_RTG.jpeg',0)

plt.imshow(images_new)
# plt.show()

for i in imgList:
    imgCurr = cv2.imread(f'{path}/{i}', 0)
    images.append(imgCurr)

trans = cv2.GaussianBlur(images_new, (5,5), 0)

images_new = cv2.equalizeHist(images_new)

cimg = cv2.cvtColor(images_new, cv2.COLOR_GRAY2BGR)
plt.imshow(cimg)
# plt.show()

_, thresh = cv2.threshold(trans, 127, 255, cv2.THRESH_TOZERO)
# thresh = cv2.Canny(trans, 40, 40)
plt.imshow(thresh,  cmap='gray')
# plt.show()

circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 1000,
                            param1=50, param2=30, minRadius=200,maxRadius=0)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

plt.imshow(cimg)
plt.show()
