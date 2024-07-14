import cv2
import numpy as np
import math
import padding as pd

class RobertsOperator():
    def __init__(self, img) -> None:
        self.prefab = pd.padding(img)
        self.robert = np.zeros(img.shape)
    def r1(self,i,j):
        r1 =  -self.prefab[i][j] + self.prefab[i+1][j+1]
        return (r1**2)
    def r2(self,i,j):
        r2 =  self.prefab[i+1][j] - self.prefab[i][j+1]
        return (r2**2)
    def compute(self,threshold):
        for i in range(self.robert.shape[0]):
            for j in range(self.robert.shape[1]):
                gradient = (math.sqrt(self.r1(i+1,j+1)+self.r2(i+1,j+1)))
                if(gradient < threshold):self.robert[i][j]=255
        cv2.imwrite("RobertsOperator({}).png".format(threshold),self.robert)
class PSF_Operator():
    def __init__(self, img) -> None:
        self.prefab = pd.padding(img)
        self.shape = img.shape
        self.kernel_1 = np.array([(-1,-1),(-1,0),(-1,1),( 1,-1),( 1,0),( 1,1)])
        self.kernel_2 = np.array([(-1,-1),(0,-1),(1,-1),(-1, 1),(0, 1),( 1,1)])
    def prewitt(self,i,j):
        p1=0
        p2=0
        for ite in self.kernel_1:
            x,y = ite
            if(x==-1):p1-=self.prefab[i+x][j+y]
            if(x== 1):p1+=self.prefab[i+x][j+y]
        for ite in self.kernel_2:
            x,y = ite
            if(y==-1):p2-=self.prefab[i+x][j+y]
            if(y== 1):p2+=self.prefab[i+x][j+y]
        return (math.sqrt(p1**2+p2**2))
    def compute_P(self,threshold):
        arr = np.zeros(self.shape)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                gradient = self.prewitt(i+1,j+1)
                if(gradient < threshold):arr[i][j]=255
        cv2.imwrite("PrewittOperator({}).png".format(threshold),arr)
    def FreiChen(self,i,j):
        f1=0
        f2=0
        for ite in self.kernel_1:
            x,y = ite
            if(x ==-1):
                if(y==0):f1-=(math.sqrt(2))*self.prefab[i+x][j+y]
                else : f1-= self.prefab[i+x][j+y]
            if(x == 1):
                if(y==0):f1+=(math.sqrt(2))*self.prefab[i+x][j+y]
                else : f1+= self.prefab[i+x][j+y]
        for ite in self.kernel_2:
            x,y = ite
            if(y ==-1):
                if(x==0):f2-=(math.sqrt(2))*self.prefab[i+x][j+y]
                else : f2-= self.prefab[i+x][j+y]
            if(y == 1):
                if(x==0):f2+=(math.sqrt(2))*self.prefab[i+x][j+y]
                else : f2+= self.prefab[i+x][j+y]
        return (math.sqrt(f1**2+f2**2))
    def compute_F(self,threshold):
        arr = np.zeros(self.shape)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                gradient = self.FreiChen(i+1,j+1)
                if(gradient < threshold):arr[i][j]=255
        cv2.imwrite("Frei&ChenOperator({}).png".format(threshold),arr)
    def Sobel(self,i,j):
        f1=0
        f2=0
        for ite in self.kernel_1:
            x,y = ite
            if(x ==-1):
                if(y==0):f1-=2*self.prefab[i+x][j+y]
                else : f1-= self.prefab[i+x][j+y]
            if(x == 1):
                if(y==0):f1+=2*self.prefab[i+x][j+y]
                else : f1+= self.prefab[i+x][j+y]
        for ite in self.kernel_2:
            x,y = ite
            if(y ==-1):
                if(x==0):f2-=2*self.prefab[i+x][j+y]
                else : f2-= self.prefab[i+x][j+y]
            if(y == 1):
                if(x==0):f2+=2*self.prefab[i+x][j+y]
                else : f2+= self.prefab[i+x][j+y]
        return (math.sqrt(f1**2+f2**2))
    def compute_S(self,threshold):
        arr = np.zeros(self.shape)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                gradient = self.Sobel(i+1,j+1)
                if(gradient < threshold):arr[i][j]=255
        cv2.imwrite("SobelOperator({}).png".format(threshold),arr)
        
class Kirsch_Operator():
    def __init__(self, img) -> None:
        self.prefab = pd.padding(img)
        self.shape = img.shape
        self.kernel = np.array([(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]) #必須照順序繞一圈寫,不然會錯誤
    def compute(self,threshold):
        arr = np.zeros(self.shape)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                gradient = self.kn(i+1,j+1)
                if(gradient < threshold):arr[i][j]=255
        cv2.imwrite("KirschOperator({}).png".format(threshold),arr)

    def kn(self,i,j):
        k=np.zeros(8,np.uint)
        for a in range(8):
            count = 0
            for b in range(5):
                while count<3:
                    if a+count < (len(self.kernel)):
                        x,y = self.kernel[a+count]
                        k[a] += 5*self.prefab[i+x][j+y]
                    else : 
                        x,y = self.kernel[a+count-len(self.kernel)]
                        k[a] += 5*self.prefab[i+x][j+y]
                    count+=1
                if(a+count-len(self.kernel)+b)<0:
                    x,y = self.kernel[a+count-len(self.kernel)+b+8]
                    k[a] -= (3*self.prefab[i+x][j+y])
                else: 
                    x,y = self.kernel[a+count-len(self.kernel)+b]
                    k[a] -= (3*self.prefab[i+x][j+y])
        return(max(k))
    
class Robinson_Operator():
    def __init__(self, img) -> None:
        self.prefab = pd.padding(img)
        self.shape = img.shape
        self.kernel_1 = np.array([(-1,1),(0,1),(1,1),(1,-1),(0,-1),(-1,-1)]) #必須照順序繞一圈寫,不然會錯誤
        self.kernel_2 = np.array([(-1,0),(-1,1),(0,1),(1,0),(1,-1),(0,-1)]) 
        self.kernel_3 = np.array([(-1,-1),(-1,0),(-1,1),(1,1),(1,0),(1,-1)]) 
        self.kernel_4 = np.array([(0,-1),(-1,-1),(-1,0),(0,1),(1,1),(1,0)]) 
        self.kernel_assemble=[self.kernel_1, self.kernel_2, self.kernel_3, self.kernel_4]
    def compute(self,threshold):
        arr = np.zeros(self.shape)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                gradient = self.Rn(i+1,j+1)
                if(gradient < threshold):arr[i][j]=255
        cv2.imwrite("RobinsonOperator({}).png".format(threshold),arr)
    def Rn(self,i,j):
        R=np.zeros(8,np.int64) 
        for circle in range(4):
            for num in range(6):
                if num==1:
                    x,y=self.kernel_assemble[circle][num]
                    R[circle] += 2*self.prefab[i+x][j+y]
                if num==4:
                    x,y=self.kernel_assemble[circle][num]
                    R[circle] -= 2*self.prefab[i+x][j+y]
                if num<3 and num!=1:
                    x,y=self.kernel_assemble[circle][num]
                    R[circle] += self.prefab[i+x][j+y]
                if num>=3 and num!=4:
                    x,y=self.kernel_assemble[circle][num]
                    R[circle] -= self.prefab[i+x][j+y]
        for n in range(4):
            R[7-n]=-1*R[n]
        return(max(R))
    
class  NevatiaBabu():
    def __init__(self, img) -> None:
        self.shape = img.shape
        self.prefab = pd.padding(pd.padding(img))
        self.k0 = np.array([
            [100, 100, 100, 100, 100],
            [100, 100, 100, 100, 100],
            [0, 0, 0, 0, 0],
            [-100, -100, -100, -100, -100],
            [-100, -100, -100, -100, -100],
        ])
        self.k1 = np.array([
            [100, 100, 100, 100, 100],
            [100, 100, 100, 78, -32],
            [100, 92, 0, -92, -100],
            [32, -78, -100, -100, -100],
            [-100, -100, -100, -100, -100]
        ])
        self.k2 = np.array([
            [100, 100, 100, 32, -100],
            [100, 100, 92, -78, -100],
            [100, 100, 0, -100, -100],
            [100, 78, -92, -100, -100],
            [100, -32, -100, -100, -100]
        ])
        self.k3 = np.array([
            [-100, -100, 0, 100, 100],
            [-100, -100, 0, 100, 100],
            [-100, -100, 0, 100, 100],
            [-100, -100, 0, 100, 100],
            [-100, -100, 0, 100, 100]
        ])
        self.k4 = np.array([
            [-100, 32, 100, 100, 100],
            [-100, -78, 92, 100, 100],
            [-100, -100, 0, 100, 100],
            [-100, -100, -92, 78, 100],
            [-100, -100, -100, -32, 100]
        ])
        self.k5 = np.array([
            [100, 100, 100, 100, 100],
            [-32, 78, 100, 100, 100],
            [-100, -92, 0, 92, 100],
            [-100, -100, -100, -78, 32],
            [-100, -100, -100, -100, -100]
        ])
    def Gn(self, i, j):
        n0 = np.sum(self.prefab[i-2: i + 3, j-2: j + 3] * self.k0)
        n1 = np.sum(self.prefab[i-2: i + 3, j-2: j + 3] * self.k1)
        n2 = np.sum(self.prefab[i-2: i + 3, j-2: j + 3] * self.k2)
        n3 = np.sum(self.prefab[i-2: i + 3, j-2: j + 3] * self.k3)
        n4 = np.sum(self.prefab[i-2: i + 3, j-2: j + 3] * self.k4)
        n5 = np.sum(self.prefab[i-2: i + 3, j-2: j + 3] * self.k5)
        G = np.max([n0, n1, n2, n3, n4, n5])
        return G
    def compute(self,threshold):
        arr = np.zeros(self.shape)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                gradient = self.Gn(i+2,j+2)
                if(gradient < threshold):arr[i][j]=255
        cv2.imwrite("Nevatia&BabuOperator({}).png".format(threshold),arr)
def main():
    img = cv2.imread('lena.bmp',0)
    RobertsOperator(img).compute(12)
    PSF_Operator(img).compute_P(24)
    PSF_Operator(img).compute_S(38)
    PSF_Operator(img).compute_F(30)
    Kirsch_Operator(img).compute(135)
    Robinson_Operator(img).compute(43)
    NevatiaBabu(img).compute(12500)

if __name__ == '__main__':
    main()
    
