import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import butter,filtfilt
from scipy.signal import find_peaks

def readImages(path):
    images=[]
    imgList = os.listdir(path)
    for i in imgList:
        imgCurr = cv2.imread(f'{path}/{i}',0)
        images.append(imgCurr)
    return images

def prepareImg(img):
    kernel = np.ones((5,5),np.uint8)
    img = cv2.equalizeHist(img)
    img = cv2.erode(img,kernel,iterations = 2)
    img = cv2.dilate(img,kernel,iterations = 2)
    img = cv2.erode(img,kernel,iterations = 4)


folder_path = './pics/crop_test'
images = readImages(folder_path)

j = 0
for img in images:
    img_or = img
    prepareImg(img)

    x_list = np.sum(img, 0)

    xp = np.linspace(0, len(img[0])-1, len(img[0]))

    p10x = np.poly1d(np.polyfit(xp, x_list, 15))
    p10x = p10x(xp)

    peaks, _ = find_peaks(p10x)

    # ind = np.where(x_list == max(x_list[i] for i in peaks))[0][0]
    # ind = np.where(peaks == ind)[0][0]
    # ind = np.where(x_list == sorted(x_list[i] for i in peaks))
    # print(ind)
    print(type(sorted(x_list[i] for i in peaks)))
    print(type())

    if(len(peaks)):
        if(ind > 0):
            x1 = peaks[ind-1]
            print(x1)
            margines = int(len(img_or[0])*0.05)
            while True:
                if(x1 - margines >= 0):
                    x1 -= margines
                    print(x1)
                    break
                margines -= 1
        else:
            x1 = 0

        if(ind < len(img_or)-1):
            x2 = peaks[ind+1]
            margines = int(len(img_or[0])*0.05)
            while True:
                if(x2 + margines <= len(img_or[0])):
                    x2 += margines
                    break
                margines -= 1
        else:
            x2 = len(img_or[0])-1

        im1 = img_or[0:(len(img_or)-1), x1:x2]

        cv2.imshow("cropped_OX", im1)
        cv2.imshow("original", img_or)
    else:
        print("Err0X -- Cannot crop image:", imgList[j])

    y_list = []
    for i in im1:
        y_list.append(i.sum())

    yp = np.linspace(0, len(im1)-1, len(im1))
    p10y = np.poly1d(np.polyfit(yp, y_list, 10))

    p10y = p10y(yp)
    peaks2, _ = find_peaks(p10y, height=0)

    plt.subplot(121)
    plt.plot(xp, x_list, '.', xp, p10x, '-')
    plt.plot(peaks, p10x[peaks], "x")
    plt.title('OX')
    plt.subplot(122)
    plt.title('OY')
    plt.plot(yp, y_list, '.', yp, p10y, '-')
    plt.plot(peaks2, p10y[peaks2], "x")

    # margines = 30
    # if len(peaks2)>0:
    #     if(peaks2[0]-margines):
    #         peaks2[0]-=margines
    #     if(peaks2[-1])+margines < len(img_or):
    #         peaks2[-1]+=margines
    #
    #     im2 = im1[(peaks2[0]):(peaks2[-1]), 0:(len(im1[0])-1)]
    #     cv2.imshow("cropped2", im2)
    plt.show()

    j+=1
