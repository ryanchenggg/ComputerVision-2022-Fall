import cv2
import numpy as np
def binarize(img):
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i][j]>127:img[i][j]=255
            else:img[i][j]=0

def DownSampling(img):
    arr = np.zeros((img.shape[0]//8+2, img.shape[1]//8+2),np.uint8)
    for i in range(1, arr.shape[0]-1):
        for j in range(1, arr.shape[1]-1):
            arr[i][j]=img[(i-1)*8][(j-1)*8]
    return arr

def Yokoi(img,i,j):
    if(img[i][j]==0):return ' '
    if(img[i-1][j-1]!=0 and img[i-1][j]!=0 and img[i-1][j+1]!=0 
       and img[i][j-1]!=0 and img[i][j+1]!=0 
       and img[i+1][j-1]!=0 and img[i+1][j]!=0 and img[i+1][j+1]!=0):
       return '5'
    count=0
    #right
    if(img[i][j+1]!=0):
        if(img[i-1][j]==0 or img[i-1][j+1]==0):count+=1
    #top
    if(img[i-1][j]!=0):
        if(img[i-1][j-1]==0 or img[i][j-1]==0):count+=1
    #left
    if(img[i][j-1]!=0):
        if(img[i+1][j-1]==0 or img[i+1][j]==0):count+=1
    #bottom
    if(img[i+1][j]!=0):
        if(img[i+1][j+1]==0 or img[i][j+1]==0):count+=1
    
    if(count==0):return '0'
    return str(count)
    

   


def main():
    img = cv2.imread('lena.bmp',0)
    binarize(img)
    DownSample=DownSampling(img) #DownSample.shape=(66,66)

    path = 'result.txt'
    with open(path, 'w') as f:
        for i in range(1, DownSample.shape[0]-1):
            for j in range(1, DownSample.shape[1]-1):
                f.write(Yokoi(DownSample,i,j))
            f.write('\n')
    
if __name__ == '__main__':
    main()
