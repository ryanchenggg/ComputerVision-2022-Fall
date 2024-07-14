import cv2
import numpy as np

def dilation(img,kernel):
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i][j]!=0:
                max = 0
                for ite in kernel:
                    x, y = ite
                    if x+i>=0 and x+i<img.shape[0] and y+j>=0 and y+j<img.shape[1]:
                        if img[x+i][y+j]>max: max=img[x+i][y+j]
                arr[i][j]=max
    return arr
def erosion(img,kernel):
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            count = True
            min = np.iinfo(np.int64).max
            for ite in kernel:
                if(count==False):break
                x, y = ite
                if x+i < 0 or x+i>=img.shape[0] or y+j<0 or y+j>=img.shape[1]:
                    count=False
                    break    
                if img[i+x][j+y]==0:
                    count=False
                elif img[i+x][j+y]<min: min=img[i+x][j+y]
            if count == True: arr[i][j]=min
    return arr
def opening(img,kernel):
    arr = np.zeros(img.shape, np.uint8)
    arr = erosion(img,kernel)
    return dilation(arr,kernel)
def closing(img,kernel):
    arr = np.zeros(img.shape, np.uint8)
    arr = dilation(img, kernel)
    return erosion(arr, kernel)
def main():
    kernel = [[-2, -1], [-2, 0], [-2, 1],
              [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
              [0, -2], [0, -1], [0, 0], [0, 1], [0, 2],
              [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
              [2, -1], [2, 0], [2, 1]]
    img = cv2.imread('lena.bmp',0)
    dialtion_img = dilation(img,kernel)
    erosion_img = erosion(img,kernel)
    opening_img = opening(img,kernel)
    closing_img = closing(img,kernel)
    

    
    cv2.imwrite('dialtion.png',dialtion_img)
    cv2.imwrite('erosion.png',erosion_img)
    cv2.imwrite('opening.png',opening_img)
    cv2.imwrite('closing.png',closing_img)


if __name__ == '__main__':
    main()
