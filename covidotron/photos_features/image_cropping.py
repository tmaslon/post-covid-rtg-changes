import cv2
import os
import sys
from matplotlib import pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import butter,filtfilt
from scipy.signal import find_peaks

def readImages(path):
    _images = []
    imgList = os.listdir(path)
    for i in imgList:
        imgCurr = cv2.imread(f'{path}/{i}', 0)
        _images.append(imgCurr)
    return _images, imgList

def prepareImg(img_t):
    kernel = np.ones((5, 5), np.uint8)
    img_t = cv2.equalizeHist(img_t)
    img_t = cv2.erode(img_t, kernel, iterations=2)
    img_t = cv2.dilate(img_t, kernel, iterations=2)
    img_t = cv2.erode(img_t, kernel, iterations=4)
    return img_t

def find_nearest(peaks_t, values):
    ind_t = 0
    middle = int(len(values)/2)
    for i in range(1, len(peaks_t)):
        if abs(peaks_t[i]-middle) < abs(peaks_t[ind_t]-middle):
            ind_t = i
    return ind_t

def main():
    show_all = 0
    if len(sys.argv) > 4:
        print("Too many arguments. For help -h .")
        return
    if len(sys.argv) == 1:
        print("Too few arguments. For help -h .")
        return

    if len(sys.argv[1]) == '-h':
        print("Syntax: python image_cropping.py <source_path> <destination_path> <optional>")
        print("<optional> \t - 1 if you want to plot and display images")
    else:
        folder_path = sys.argv[1]
        images, imgList = readImages(folder_path)

        j = 0
        for img in images:
            img_or = img
            img = prepareImg(img)

            x_list = np.sum(img, 0)

            xp = np.linspace(0, len(img[0])-1, len(img[0]))

            p10x = np.poly1d(np.polyfit(xp, x_list, 10))
            p10x = p10x(xp)

            peaks, _ = find_peaks(p10x)

            ind = find_nearest(peaks, x_list)

            if len(peaks)>=3:
                if ind > 0:
                    x1 = peaks[ind-1]
                    margines = int(len(img_or[0])*0.05)
                    while True:
                        if x1 - margines >= 0:
                            x1 -= margines
                            break
                        margines -= 1
                else:
                    x1 = 0

                if(ind < len(img_or[0])-1):
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

                if show_all == 1:
                    cv2.imshow("cropped_OX", im1)
                    cv2.imshow("original", img_or)

            y_list = []
            for i in im1:
                y_list.append(i.sum())

            yp = np.linspace(0, len(im1)-1, len(im1))
            p10y = np.poly1d(np.polyfit(yp, y_list, 10))

            p10y = p10y(yp)
            peaks2, _ = find_peaks(p10y, height=0)

            if show_all == 1:
                plt.subplot(121)
                plt.plot(xp, x_list, '.', xp, p10x, '-')
                plt.plot(peaks, p10x[peaks], "x")
                plt.title('OX')
                plt.subplot(122)
                plt.title('OY')
                plt.plot(yp, y_list, '.', yp, p10y, '-')
                plt.plot(peaks2, p10y[peaks2], "x")

            if peaks2[0] < len(y_list)*0.3:
                margines = int(len(img_or)*0.1)
                x1 = peaks2[0]
                while True:
                    if x1 - margines >= 0:
                        x1 -= margines
                        break
                    margines -= 1
                im1 = im1[x1:(len(im1)-1), 0:(len(im1[0])-1)]

                if show_all == 1:
                    cv2.imshow("croppedOY", im1)
            if show_all == 1:
                plt.show()

            cv2.imwrite(sys.argv[2]+os.path.splitext(imgList[j])[0]+'_cropped'+os.path.splitext(imgList[j])[1], im1)
            j+=1

if __name__ == "__main__":
    main()
