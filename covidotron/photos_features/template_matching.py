import cv2
import os
from matplotlib import pyplot as plt
import numpy as np

img_ref = cv2.imread('pics/ref_image3.jpg', 0)
# img_ref = cv2.equalizeHist(img_ref)

img = cv2.imread('pics/COVID-19/covid19_30yo_female_RTG.jpeg',0)
img = cv2.equalizeHist(img)

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img_ref, None)
kp2, des2 = orb.detectAndCompute(img, None)

# imgKp1 = cv2.drawKeypoints(img_ref, kp1, None)
# imgKp2 = cv2.drawKeypoints(img, kp2, None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

good = []
for m,n in matches:
    if m.distance < 0.9*n.distance:
        good.append([m])

img2 = cv2.drawMatchesKnn(img_ref, kp1, img, kp2, good, None, flags=2)

# cv2.imshow('Kp1', imgKp1)
# cv2.imshow('Kp2', imgKp2)
# cv2.imshow('img_ref', img_ref)
# cv2.imshow('img', img)
cv2.imshow('img_draw', img2)
cv2.waitKey(0)
