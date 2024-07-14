import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class image:
    def __init__(self, img):
        self.current_row = 0
        self.current_col = 0
        self.current_label = 1
        self.arr = np.zeros((img.shape[0],img.shape[1]), dtype=np.int64) #為了存超過unit8
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                self.arr[i][j] = img[i][j]
        self.img = img

    def push(self):
        self.current_col +=1
        if(self.current_col == self.arr.shape[1]):
            self.current_row +=1
            self.current_col =0
    def back(self):
        self.current_col -=1
        if(self.current_col == -1):
            self.current_row -= 1
            self.current_col = (self.arr.shape[1]-1) #回到511
    def label(self):
        self.arr[self.current_row][self.current_col] = self.current_label
        self.current_label += 1
    def label_item(self):#if recursive -> stack overflow, so using iteratively algorithm
        while(True):
            if(self.current_row == (self.arr.shape[0]-1) and self.current_col == (self.arr.shape[1]-1)):
                if(self.arr[self.current_row][self.current_col] == 0): #若最後一格為黑
                    break
                else:
                    self.label()
                    break
            elif( self.arr[self.current_row][self.current_col] != 0): #如果pixel內為白
                self.label()
                self.push()
            else :
                self.push()
    
    #左上到右下函數功能
    def min_from_top(self):
        if(self.arr[self.current_row-1][self.current_col]==0):return
        elif(self.arr[self.current_row][self.current_col] > self.arr[self.current_row-1][self.current_col]): 
                self.arr[self.current_row][self.current_col] = self.arr[self.current_row-1][self.current_col]
    def min_from_left(self):
        if(self.arr[self.current_row][self.current_col-1]==0):return
        elif(self.arr[self.current_row][self.current_col] > self.arr[self.current_row][self.current_col-1]): 
            self.arr[self.current_row][self.current_col] = self.arr[self.current_row][self.current_col-1]
    #右下到左上函數功能
    def min_from_right(self):
        if(self.arr[self.current_row][self.current_col+1]==0):return
        elif(self.arr[self.current_row][self.current_col] > self.arr[self.current_row][self.current_col+1]): 
            self.arr[self.current_row][self.current_col] = self.arr[self.current_row][self.current_col+1]
    def min_from_bot(self):
        if(self.arr[self.current_row+1][self.current_col]==0):return
        elif(self.arr[self.current_row][self.current_col] > self.arr[self.current_row+1][self.current_col]): 
            self.arr[self.current_row][self.current_col] = self.arr[self.current_row+1][self.current_col]
    def min_body1(self): #第0列/第0行皆不適用
        self.min_from_top()
        self.min_from_left()
    def min_body2(self): #第511列/第511行皆不適用
        self.min_from_right()
        self.min_from_bot()

    def zero_checker(self):
        if(self.arr[self.current_row][self.current_col]==0):
            return True
        else : return False
    def top_down(self):
        while(True):
            if(self.current_row == (self.arr.shape[0]-1) and self.current_col == (self.arr.shape[1]-1)):#走到最後一格
                self.min_body1()
                break
            elif(self.zero_checker() is True):self.push()#遇到0的格子do nothing,直接進下一格 
            elif(self.current_row == 0):#第0列,只能比左邊
                if(self.current_row == 0 and self.current_col == 0):
                    self.push()
                else:
                    self.min_from_left()
                    self.push()
            elif(self.current_col == 0):#第0行,只能比上面
                self.min_from_top()
                self.push()
            else:#中間區塊
                self.min_body1()
                self.push() 
    def bottom_up(self):
        while(True):
            #print("({},{})".format(self.current_row,self.current_col))
            if(self.current_row == 0 and self.current_col == 0):#走到最後一格
                self.min_body2()
                break
            elif(self.zero_checker() is True):self.back()#遇到0的格子do nothing,直接進下一格
            elif(self.current_row == 511): #第511列只能比右邊
                if(self.current_row == 511 and self.current_col == 511):
                    self.back()
                else:
                    self.min_from_left()
                    self.back()
            elif(self.current_col == 511): #第511行只能比下面
                self.min_from_bot()
                self.back()
            else:                          #中間區塊
                self.min_body2()
                self.back()
    def drawing(self):
        count = []
        region = []
        for i in range(0, self.arr.shape[0]):
            for j in range(0, self.arr.shape[1]):
                if(self.arr[i][j]!=0):
                    count.append(self.arr[i][j])
                    
        for k in range(0,self.current_label):
            if(count.count(k)>500):
                region.append(k)
        for h in range(len(region)):
            X_max=0
            X_min=99999999
            Y_max=0
            Y_min=99999999
            area = 0
            centroid_x = 0
            centroid_y = 0
            for i in range(0, self.arr.shape[0]):
                for j in range(0, self.arr.shape[1]):
                    if(self.arr[i][j]==self.arrregion[h]):
                        area+=1
                        centroid_x += i*1
                        centroid_y += j*1
                        if(i > X_max):
                            X_max = i
                        if(i < X_min):
                            X_min = i
                        if(j > Y_max):
                            Y_max = j
                        if(j < Y_min):
                            Y_min = j
            centroid_x = (centroid_x//area)
            centroid_y = (centroid_y//area)
            cv2.rectangle(self.img, (Y_min, X_min), (Y_max, X_max), (255,0,0) , 2)
            cv2.line(self.img, (centroid_y - 7, centroid_x), (centroid_y + 7, centroid_x), (0, 0, 255), 3)
            cv2.line(self.img, (centroid_y, centroid_x - 7), (centroid_y ,centroid_x + 7), (0, 0, 255), 3)
            
        cv2.imshow('labeled',self.img)
        cv2.waitKey(0)
        cv2.imwrite('Connected_Components.png',self.img)

    def tester(self):
        self.label_item()
        for i in range(20):
            self.top_down()
            self.bottom_up()
        self.drawing()
        # df = pd.DataFrame(self.arr)
        # df.to_excel('output.xlsx', header=False, index=False)
        #print(self.arr.shape)
        pass

def main():
    img = cv2.imread('lena.bmp',0)
    img_transfered= np.zeros(img.shape)
    if (type(img)is np.ndarray):
        def binarize():
            for i in range(0, img.shape[0]):
                for j in range(0, img.shape[1]):
                    #print(img[i][j]) checker
                    if(img[i][j]>128):
                        img[i][j]=255
                    else:
                        img[i][j]=0
            cv2.imwrite('binarized.bmp',img)
        def histogram():
            arr = np.zeros(256, np.int64)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    arr[img[i][j]] += 1

            Intensity = np.arange(0, 256, 1)
            plt.bar(Intensity, arr)
            plt.title("Histogram")
            plt.show()
        histogram()
        binarize()
    x = image(img)
    x.tester()

if __name__ == '__main__':
    main() 

