import cv2
import numpy as np
import padding as pd

def ZeroCrossing(prefab, i, j):
    if prefab[i][j]== -1: return 255
    if prefab[i][j]== 0: return 255
    for s in range(i-1, i+2):
        for r in range(j-1, j+2):
            if prefab[s][r]==-1: return 0
    return 255
    
def Laplacian_typ1(img, threshold):
    prefab = pd.padding(img)
    arr_Laplacian = np.zeros(prefab.shape, np.int8)
    k1=np.array([
        [0, 1, 0],
        [1, -4, 1],
        [0, 1, 0]
    ])
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            gradient = ConvBy3(prefab, k1, i, j)
            if gradient>=threshold: arr_Laplacian[i][j]=1
            elif gradient <= threshold: arr_Laplacian[i][j]=-1
            else: arr_Laplacian[i][j]=0
            
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            arr[i][j] = ZeroCrossing(arr_Laplacian, i+1, j+1)
    cv2.imwrite('laplacian_1({}).png'.format(threshold),arr)
    
def Laplacian_typ2(img, threshold):
    prefab = pd.padding(img)
    arr_Laplacian = np.zeros(prefab.shape, np.int8)
    k2 = np.array([
            [1., 1, 1],
            [1, -8, 1],
            [1, 1, 1]
        ]) / 3    
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            gradient = ConvBy3(prefab, k2, i, j)
            if gradient>=threshold: arr_Laplacian[i][j]=1
            elif gradient <= threshold: arr_Laplacian[i][j]=-1
            else: arr_Laplacian[i][j]=0
            
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            arr[i][j] = ZeroCrossing(arr_Laplacian, i+1, j+1)
    cv2.imwrite('laplacian_2({}).png'.format(threshold),arr)     

def Laplacian_mini_var(img, threshold):
    prefab = pd.padding(img)
    arr_Laplacian = np.zeros(prefab.shape, np.int8)
    k3 = np.array([
            [2., -1, 2],
            [-1, -4, -1],
            [2, -1, 2]
        ]) / 3  
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            gradient = ConvBy3(prefab, k3, i, j)
            if gradient>=threshold: arr_Laplacian[i][j]=1
            elif gradient <= threshold: arr_Laplacian[i][j]=-1
            else: arr_Laplacian[i][j]=0
            
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            arr[i][j] = ZeroCrossing(arr_Laplacian, i+1, j+1)
    cv2.imwrite('laplacian_mini_var({}).png'.format(threshold),arr)   
def ConvBy3(prefab, kernel, i, j):
    gradient =  np.sum(prefab[i-1:i+2, j-1:j+2]*kernel)
    return gradient
def ConvBy11(prefab, kernel, i, j):
    gradient =  np.sum(prefab[i-5:i+6, j-5:j+6]*kernel)
    return gradient

def LaplaceOfGuassian(img, threshold):
    prefab = cv2.copyMakeBorder(img,5,5,5,5,cv2.BORDER_REPLICATE)
    arr_Laplacian = np.zeros(prefab.shape, np.int8)
    k = np.array([
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
        [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]
    ]) 
    for i in range(5, img.shape[0]-5):
        for j in range(5, img.shape[1]-5):
            gradient = ConvBy11(prefab, k, i, j)
            if gradient>=threshold: arr_Laplacian[i][j]=1
            elif gradient <= threshold: arr_Laplacian[i][j]=-1
            else: arr_Laplacian[i][j]=0
            
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            arr[i][j] = ZeroCrossing(arr_Laplacian, i+5, j+5)
    cv2.imwrite('laplacian_guassian({}).png'.format(threshold),arr)
    
def DifferenceOfGuassian(img, threshold):
    prefab = cv2.copyMakeBorder(img,5,5,5,5,cv2.BORDER_REPLICATE)
    arr_Laplacian = np.zeros(prefab.shape, np.int8)
    k =  np.array([
            [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
            [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
            [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
            [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
            [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
            [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
            [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
            [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
            [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
            [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
            [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
        ])
    for i in range(5, img.shape[0]-5):
        for j in range(5, img.shape[1]-5):
            gradient = ConvBy11(prefab, k, i, j)
            if gradient>=threshold: arr_Laplacian[i][j]=1
            elif gradient <= threshold: arr_Laplacian[i][j]=-1
            else: arr_Laplacian[i][j]=0
            
    arr = np.zeros(img.shape, np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            arr[i][j] = ZeroCrossing(arr_Laplacian, i+5, j+5)
    cv2.imwrite('Difference_guassian({}).png'.format(threshold),arr)
def main():
    img = cv2.imread('lena.bmp',0)
    # Laplacian_typ1(img, 15)
    # Laplacian_typ2(img, 15)
    # Laplacian_mini_var(img, 20)
    # LaplaceOfGuassian(img, 3000)
    # DifferenceOfGuassian(img, 1)
if __name__ == '__main__':
    main()
