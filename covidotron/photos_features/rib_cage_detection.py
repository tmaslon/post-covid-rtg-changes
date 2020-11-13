# Not working; Bad approach

import cv2
import os
from matplotlib import pyplot as plt
import numpy as np

path = 'pics/healthy'
img_ref = cv2.imread('pics/ref_image.jpg', 0)
imgList = os.listdir(path)
images = []
images_new = cv2.imread('pics/COVID-19/covid19_37yo_male_RTG.jpg',0)



for i in imgList:
    imgCurr = cv2.imread(f'{path}/{i}', 0)
    images.append(imgCurr)

trans = cv2.GaussianBlur(images_new, (5,5), 0)
cimg = cv2.cvtColor(images_new, cv2.COLOR_GRAY2BGR)
plt.imshow(cimg)
plt.show()

_, thresh = cv2.threshold(trans, 140, 255, cv2.THRESH_TOZERO)
# thresh = cv2.Canny(trans, 40, 40)
plt.imshow(thresh,  cmap='gray')
plt.show()

circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 20,
                            param1=50, param2=30, minRadius=0,maxRadius=0)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

plt.imshow(cimg)
plt.show()

# for i in images:
#     trans = cv2.GaussianBlur(i, (5,5), 0)
#     # trans = cv2.Laplacian(i, cv2.CV_64F)
#     plt.imshow(trans, cmap='gray')
#     plt.show()
#
#     _, thresh = cv2.threshold(trans, 20, 255, cv2.THRESH_BINARY)
#     plt.imshow(thresh, cmap='gray')
#     plt.show()
#
#     dilated = cv2.dilate(thresh, None, iterations=3)
#     plt.imshow(dilated)
#     plt.show()
#
#     countours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#     (x, y, w, h) = cv2.boundingRect(countours)
#     crop_img = i[y:y+h, x:x+w]
#     plt.imshow(crop_img, cmap='gray')
