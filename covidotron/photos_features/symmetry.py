import cv2
import os
from matplotlib import pyplot as plt
import numpy as np

img = cv2.imread('pics/COVID-19/covid19_30yo_female_RTG.jpeg',0)

G_X = cv2.reduce(img, 0 ,cv2.REDUCE_SUM)
G_Y = cv2.reduce(img, 1 ,cv2.REDUCE_SUM)

plt.imghow(G_X)
plt.show()
