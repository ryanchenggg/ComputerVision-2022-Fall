import cv2
import numpy as np
import matplotlib.pyplot as plt
def histogram(img):
    arr = np.zeros(256, np.int64)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            arr[img[i][j]] += 1 #arr存各intensity各數

    Intensity = np.arange(0, 256, 1)
    plt.bar(Intensity, arr)
    plt.title("Histogram")
    plt.show()
def intensity(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j]=img[i][j]//3
    cv2.imwrite('intensity.png',img)
def histogram_equalize(img):
    arr = np.zeros(256, np.int64)
    #arr2 = np.zeros(256, np.int64)
    arr_CDF = np.zeros(256, np.float16)
    Area =img.shape[0]*img.shape[1]
    #histogram first
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            arr[img[i][j]] += 1

    for i in range (1,255):
        arr[i]+=arr[i-1]
        arr_CDF[i]=arr[i]/Area

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j]=arr_CDF[img[i][j]]*255
    # #he-cdf
    # for i in range(img.shape[0]):
    #     for j in range(img.shape[1]):
    #         arr2[img[i][j]] += 1

    # for i in range (1,255):
    #     arr2[i]+=arr2[i-1]
    #     arr_CDF[i]=arr2[i]/Area

    #drawing
    Intensity = np.arange(0, 256, 1)
    plt.bar(Intensity, arr_CDF)
    plt.title("Histogram3")#CDF of original hist
    plt.show()
    histogram(img)
    cv2.imwrite('histogram_eq.png',img)
def main():
    img = cv2.imread('lena.bmp',0)
    arr1 = np.copy(img)
    histogram(arr1)#a
    intensity(arr1)
    histogram(arr1)#b
    histogram_equalize(arr1)#c
    
    
if __name__ == '__main__':
    main()