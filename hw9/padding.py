import cv2
import numpy as np

def padding(img):
    AfterPadding = np.zeros((img.shape[0]+2,img.shape[1]+2))
    for i in range (1, img.shape[0]+1):
        for j in range (1, img.shape[1]+1):
            AfterPadding[i][j]=img[i-1][j-1]
    AfterPadding[[0],:] = AfterPadding[[1],:]
    AfterPadding[[AfterPadding.shape[0]-1],:] = AfterPadding[[AfterPadding.shape[0]-2],:]
    AfterPadding[:,[0]] = AfterPadding[:,[1]]
    AfterPadding[:,[AfterPadding.shape[1]-1]] = AfterPadding[:,[AfterPadding.shape[1]-2]]
    return AfterPadding
def main():
    pass
if __name__ == '__main__':
    main()
