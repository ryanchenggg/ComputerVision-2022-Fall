import cv2
import numpy as np

img = cv2.imread('./lena.bmp')


img_transfered= np.zeros(img.shape)

img_height = img.shape[0]
img_width = img.shape[1]

#upside-down
def UpsideDown():
    for i in range(0, img_height):
        for j in range(0, img_width):
            img_transfered[i][j]=img[img_height-i-1][j]
    cv2.imwrite('upside-down_lena.bmp',img_transfered)

#right-side-left
def RightSideLeft():
    for i in range(0, img_height):
        for j in range(0, img_width):
            img_transfered[i][j]=img[i][img_width-j-1]
    cv2.imwrite('right-side-down_lena.bmp',img_transfered)

#diagonally flip
def DiagonallyFlip():
    for i in range(0, img_height):
        for j in range(0, img_width):
            img_transfered[i][j]=img[img_height-i-1][img_width-j-1]
    cv2.imwrite('diagonally-flip_lena.bmp',img_transfered)



#############Part2.###############
#rotate
def rotate(img, angle , center=None, scale=1.0):
    img_height = img.shape[0]
    img_width = img.shape[1]   
    
    if center is None:
        center = (img_height/2, img_width/2)
    
    #rotate
    M = cv2.getRotationMatrix2D(center,angle,scale)
    rotated = cv2.warpAffine(img, M, (img_height, img_width))

    return rotated

img_rotated = rotate(img, 360-45)
cv2.imwrite('rotated.bmp',img_rotated)


# shrink(resize)
scale = 2
img_transfered= np.zeros((img.shape[0]//scale, img.shape[1]//scale, 3))

def Resizer(img, shape, scale):
    height = shape[0]
    width = shape[1]
    re_height = shape[0]//scale
    re_width = shape[1]//scale
    #img_transfered= np.zeros((img.shape[0]//scale, img.shape[1]//scale))

    for i in range(0,re_height):
        for j in range(0,re_width):
            for k in range (scale):
                img_transfered[i][j] += img[2*i+k][2*j]
                img_transfered[i][j] += img[2*i][2*j+k]

    #print(img_transfered[0][0])

Resizer(img, img.shape, 2)
img_transfered=img_transfered//4   
#print(img_transfered[0][0]) check if resize success
cv2.imwrite('resized.bmp',img_transfered)


#reload lena.bmp by grey scale

img = cv2.imread('lena.bmp',0)
def binarize():
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            #print(img[i][j]) checker
            if(img[i][j]>128):
                img[i][j]=255
            else:
                img[i][j]=0

    cv2.imwrite('binarized.bmp',img)

binarize()








