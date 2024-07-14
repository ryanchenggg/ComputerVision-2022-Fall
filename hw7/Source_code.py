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
    if(img[i][j]==0):return 0
    if(img[i-1][j-1]!=0 and img[i-1][j]!=0 and img[i-1][j+1]!=0 
       and img[i][j-1]!=0 and img[i][j+1]!=0 
       and img[i+1][j-1]!=0 and img[i+1][j]!=0 and img[i+1][j+1]!=0):
       return 5
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
    #if(count==0):return 0
    return int(count)
    
def YokoiWholeImg(img):
    arr = np.zeros(img.shape, np.uint8)
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            arr[i][j] = Yokoi(img,i,j)
            #print(arr[i][j],end=" ")
    return arr
    
def Marking(img):
    arr = np.zeros(img.shape, np.uint8)
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            if img[i][j] == 1 : 
                if (img[i-1][j]==1 or img[i][j-1]==1 or
                    img [i][j+1]==1 or img[i+1][j]==1):
                    arr[i][j]=100 #set p
    
    return arr
def unPadding(img):
    arr = np.zeros((64,64), np.uint8)
    for i in range(0, 64):
        for j in range(0, 64):
            arr[i][j]=img[i+1][j+1]
    return arr

def main():
    img = cv2.imread('lena.bmp',0)
    binarize(img)
    Origin_img = DownSampling(img) #shape=(66,66)
    #thinning
    count =0
    NoDuplicate = True
    while(NoDuplicate):
        Yokoi_img = YokoiWholeImg(Origin_img)
        Marked_img = Marking(Yokoi_img)
        SetOrigin =  Origin_img.copy()
        for i in range(1, 65):
            for j in range(1, 65):
                if Marked_img[i][j] == 100:
                    ForYokoi =  Origin_img.copy()
                    ForYokoi[i][j] = Yokoi(Origin_img,i,j)
                    if(ForYokoi[i][j]==1):  
                        Origin_img[i][j] = 0
        count +=1 
        if(SetOrigin ==  Origin_img).all():
            print(count)
            NoDuplicate=False
    unpadOrigin = unPadding(Origin_img)
    cv2.imwrite('Thinning.png', unpadOrigin)

               
    
if __name__ == '__main__':
    main()
