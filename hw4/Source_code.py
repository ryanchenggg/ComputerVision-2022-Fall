import cv2
import numpy as np

def binarize(img):
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i][j]>127:img[i][j]=255
            else:img[i][j]=0
def dilation(img,kernel):
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i][j]==255:
                for ite in kernel:
                    x, y = ite
                    if x+i>=0 and x+i<img.shape[0] and y+j>=0 and y+j<img.shape[1]:
                        arr[x+i][y+j]=255
    return arr
def erosion(img,kernel):
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
                count = 0
                for ite in kernel:
                    x, y = ite
                    if x+i < 0 or x+i>=img.shape[0] or y+j<0 or y+j>=img.shape[1]:
                        break    
                    elif img[i+x][j+y]==255:
                        count+=1
                if count == len(kernel): arr[i][j]=255
    return arr
def opening(img,kernel):
    arr = np.zeros(img.shape, np.uint8)
    arr = erosion(img,kernel)
    return dilation(arr,kernel)
def closing(img,kernel):
    arr = np.zeros(img.shape, np.uint8)
    arr = dilation(img, kernel)
    return erosion(arr, kernel)
def HNM(img,J,K):
    img_c = contrary(img)
    arr1 = erosion(img,J)
    arr2 = erosion(img_c,K)
    arr = np.zeros(img.shape, np.uint8)
    for i in range (0,img.shape[0]):
        for j in  range(0, img.shape[1]):
            if arr1[i][j]==255 and arr2[i][j]==255:arr[i][j]=255
    return arr
def contrary(img):
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0,img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i][j]==0:arr[i][j]=255
    return arr
def main():
    kernel = [[-2, -1], [-2, 0], [-2, 1],
              [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
              [0, -2], [0, -1], [0, 0], [0, 1], [0, 2],
              [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
              [2, -1], [2, 0], [2, 1]]
    img = cv2.imread('lena.bmp',0)
    binarize(img)
    dialtion_img = dilation(img,kernel)
    erosion_img = erosion(img,kernel)
    opening_img = opening(img,kernel)
    closing_img = closing(img,kernel)
    
    J_Kernel = [[0, -1], [0, 0], [1, 0]]
    K_Kernel = [[-1, 0], [-1, 1], [0, 1]]

    hit_and_miss = HNM(img,J_Kernel,K_Kernel)
    
    cv2.imwrite('dialtion.png',dialtion_img)
    cv2.imwrite('erosion.png',erosion_img)
    cv2.imwrite('opening.png',opening_img)
    cv2.imwrite('closing.png',closing_img)
    cv2.imwrite('hit_and_miss.png',hit_and_miss)

if __name__ == '__main__':
    main()
