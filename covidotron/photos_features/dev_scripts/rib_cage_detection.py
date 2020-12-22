# Not working; Bad approach

import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import butter,filtfilt
from scipy.signal import find_peaks

# pipline of transformation; far from perfect ----------------
# path = 'pics/healthy'
# img_ref = cv2.imread('pics/ref_image.jpg', 0)
# imgList = os.listdir(path)
# images = []
# imgages_new= cv2.imread('pics/COVID-19/covid19_30yo_female_RTG.jpeg',0)
#
# plt.imshow(images_new)
# plt.show()

# for i in imgList:
#     imgCurr = cv2.imread(f'{path}/{i}', 0)
#     images.append(imgCurr)

# trans = cv2.GaussianBlur(images_new, (5,5), 0)
#
# images_new = cv2.equalizeHist(images_new)
#
# cimg = cv2.cvtColor(images_new, cv2.COLOR_GRAY2BGR)
# plt.imshow(cimg)
# # plt.show()
#
# _, thresh = cv2.threshold(trans, 127, 255, cv2.THRESH_TOZERO)
# # thresh = cv2.Canny(trans, 40, 40)
# plt.imshow(thresh,  cmap='gray')
# # plt.show()
#
# circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 1000,
#                             param1=50, param2=30, minRadius=200,maxRadius=0)
# circles = np.uint16(np.around(circles))
# for i in circles[0,:]:
#     # draw the outer circle
#     cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#     # draw the center of the circle
#     cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
#
# plt.imshow(cimg)
# ------------------------------------------------------------

# corner Harris detection
filename = 'pics/COVID-19/covid19_65yo_female_RTG.jpeg'
img = cv2.imread(filename,0)

kernel = np.ones((5,5),np.uint8)

img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
img = cv2.equalizeHist(img)
img = cv2.erode(img,kernel,iterations = 1)
img = cv2.dilate(img,kernel,iterations = 1)

# img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#             cv2.THRESH_BINARY,11,2)

ret,img = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
# img = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
img = np.uint8(img)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = np.float32(img)
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# plt.imshow(img, cmap='gray')
# plt.show()

x_list = np.sum(img, 0)

y_list = []
for i in img:
    y_list.append(i.sum())

f = np.poly1d(x_list)

plt.subplot(121)
plt.plot(x_list)
# plt.scatter(indices, x_list[indices])
plt.title('OX')
plt.subplot(122)
plt.title('OY')
plt.plot(y_list)

plt.show()

