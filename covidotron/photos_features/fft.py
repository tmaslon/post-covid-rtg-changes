import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os
import cv2

path = 'path/'                  # ścieżka do folderu ze zdjęciami
imgList = os.listdir(path)

images = []                     # lista obiektów obrazów

for i in imgList:
    imgCurr = Image.open(f'{path}/{i}').convert('L')
    images.append(imgCurr)

i = 0
save = True                     # on/off zapisywanie do ścieżki
plot = True                     # on/off wyświetlanie obrazka w oknie
save_path = 'path/'             # ścieżka do zapisywania obrazów
for img in images:
    npimg = np.asarray(img)
    f = np.fft.fft2(npimg)
    fshift = np.fft.fftshift(f)
    afshift = np.abs(fshift)
    magnitude_spectrum = 20*np.log(afshift)

    if plot is True:
        plt.subplot(121)
        plt.imshow(npimg, cmap='gray', vmin=0, vmax=255)
        # zakłada się że obrazki nie zawierają spacji, a "_"
        plt.title(os.path.splitext(imgList[i])[0].replace('_', ' ')), plt.xticks([]), plt.yticks([])
        plt.subplot(122)
        plt.imshow(magnitude_spectrum, cmap='gray')
        plt.title('FFT'), plt.xticks([]), plt.yticks([])
        plt.show()

    if save is True:
        plt.savefig(save_path + os.path.splitext(imgList[i])[0] + '_fft.png')
    i+=1
