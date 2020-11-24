import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
import xlsxwriter as xl

images = []

workbook = xl.Workbook('histogram_results.xlsx')

# path = ['pics/cut_all/healthy', 'pics/cut_all/COVID-19']
path = ['../../../covid_samples/Zdrowe/wybrane', '../../../covid_samples/COVID-19/wybrane']
imgList_h = os.listdir(path[0])
imgList_c = os.listdir(path[1])

health_num = 0

for i in imgList_h:
    imgCurr = cv2.imread(f'{path[0]}/{i}', 0)
    images.append(imgCurr)
    health_num += 1
for i in imgList_c:
    imgCurr = cv2.imread(f'{path[1]}/{i}', 0)
    images.append(imgCurr)

imgList_merge = imgList_h + imgList_c

plot = False
save = False

filter = [False, True]

a = 1

# print("Healthy --------------")
for k in filter:
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 1, 'Healthy')
    worksheet.write(0, 2, 'COVID-19')
    b = 1
    for i in range(0, len(images)):
        img = images[i]

        if k is True:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            img = clahe.apply(img)
        # img = cv2.equalizeHist(img)

        h = [(img == v).sum() for v in range(256)]
        h = np.array(h)
        norm_h = h/h.sum()

        cumul_h = np.zeros((256,))
        for j in range(256):
            cumul_h[j] = norm_h[j] + cumul_h[j-1]

        if( i == health_num ):
            # print("COVID-19 -------------")
            a = a-health_num
            b = 2

        a += 1

        h2 = cumul_h[255] - cumul_h[126]
        # print(imgList_merge[i], '\t', h2)
        worksheet.write(i+1, 0, imgList_merge[i])
        worksheet.write(i+1, b, h2)

        if plot is True:
            plt.subplot(121)
            plt.imshow(img, cmap='gray', vmin=0, vmax=255)
            plt.title(os.path.splitext(imgList_merge[i])[0].replace('_', ' '))
            plt.subplot(122)
            plt.bar(range(256), cumul_h)
            # plt.hist(img.ravel(), 256, [0, 256])
            plt.show()
        if save is True:
            plt.savefig('pics/cumul_histogram/' + os.path.splitext(imgList_merge[i])[0] + '.png')

workbook.close()
print("------- DONE -------")
