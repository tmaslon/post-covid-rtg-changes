import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import butter,filtfilt
from scipy.signal import find_peaks

# filename = 'pics/COVID-19/covid19_30yo_female_RTG.jpeg'
filename = 'pics/COVID-19/covid19_43yo_male_RTG.jpg'
# filename = 'pics/COVID-19/covid19_37yo_male_RTG.jpg'
# filename = 'pics/COVID-19/covid19_65yo_female_RTG.jpeg'
# filename = 'pics/COVID-19/covid19_73yo_female_RTG.jpg'

img = cv2.imread(filename,0)
img_or = img

kernel = np.ones((5,5),np.uint8)

# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
img = cv2.equalizeHist(img)
img = cv2.erode(img,kernel,iterations = 2)
img = cv2.dilate(img,kernel,iterations = 2)

plt.imshow(img, cmap='gray')
# plt.show()

# img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#             cv2.THRESH_BINARY,11,2)

# ret,img = cv2.threshold(img,180,255,cv2.THRESH_TRUNC)
# img = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
# img = np.uint8(img)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = np.float32(img)
# img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# ret,img = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
img = cv2.erode(img,kernel,iterations = 4)
# img = cv2.dilate(img,kernel,iterations = 4)
# img = cv2.equalizeHist(img)

# ret,img = cv2.threshold(img,180,255,cv2.THRESH_TOZERO)



plt.imshow(img, cmap='gray')
# plt.show()

x_list = np.sum(img, 0)

y_list = []
for i in img:
    y_list.append(i.sum())

xp = np.linspace(0, len(img[0])-1, len(img[0]))
yp = np.linspace(0, len(img)-1, len(img))


p10x = np.poly1d(np.polyfit(xp, x_list, 15))
p10y = np.poly1d(np.polyfit(yp, y_list, 10))

p10x = p10x(xp)
p10y = p10y(yp)

peaks, _ = find_peaks(p10x, height=max(x_list)/2)
# ---- subploty -------------
plt.subplot(121)
plt.plot(xp, x_list, '.', xp, p10x, '-')
plt.plot(peaks, p10x[peaks], "x")
plt.title('OX')
plt.subplot(122)
plt.title('OY')
plt.plot(yp, y_list, '.', yp, p10y, '-')
# ---------------------------
plt.show()

margines1 = 10
margines2 = 10
while True:
    if peaks[0]-margines1:
        break
    margines1-=5
peaks[0]-=margines1

while True:
    if (peaks[-1]+margines2) < len(img_or[0]):
        break
    margines2-=5
peaks[-1]+=margines2

im1 = img_or[0:(len(img_or)-1), peaks[0]:peaks[-1]]

cv2.imshow("cropped", im1)
cv2.imshow("original", img_or)

y_list2 = []
for i in im1:
    y_list2.append(i.sum())

yp2 = np.linspace(0, len(im1)-1, len(im1))
p10y2 = np.poly1d(np.polyfit(yp2, y_list2, 10))

p10y2 = p10y2(yp2)
peaks2, _ = find_peaks(p10y2, height=0)

plt.subplot(121)
plt.plot(xp, x_list, '.', xp, p10x, '-')
plt.title('OX')
plt.subplot(122)
plt.title('OY')
plt.plot(yp2, y_list2, '.', yp2, p10y2, '-')
plt.plot(peaks2, p10y2[peaks2], "x")
print(peaks2)

margines = 30
if len(peaks2)>0:
    if(peaks2[0]-margines):
        peaks2[0]-=margines
    if(peaks2[-1])+margines < len(img_or):
        peaks2[-1]+=margines

    im2 = im1[(peaks2[0]):(peaks2[-1]), 0:(len(im1[0])-1)]
    cv2.imshow("cropped2", im2)
plt.show()
