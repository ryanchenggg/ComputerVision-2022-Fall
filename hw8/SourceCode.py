import cv2
import numpy as np
import hw5
import random
import math
def GetGaussianNoise(img, amplitude):
    GaussianNoise = img.copy()
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            GaussianNoise[i][j] = int(img[i][j]+amplitude*random.gauss(0,1))
            if GaussianNoise[i][j]>255:GaussianNoise[i][j]=255
    return GaussianNoise
def GetSaltAndPepper(img, threshold):
    SaltAndPepper = img.copy()
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            rand = random.uniform(0,1)
            if rand < threshold: SaltAndPepper[i][j]=0
            elif rand > (1-threshold): SaltAndPepper[i][j]=255
            # else do nothing
    return SaltAndPepper
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
def IBUF(img,i,j,n):
    n=n//2
    sum = img[i][j]
    for s in range (1,n+1):#each column add elements by n times
        sum+=img[i-s][j]
        sum+=img[i+s][j]
    return sum  
def BoxFilterByN(img, n):
    k = (n-1)//2 #init point(k,k)
    back = np.zeros((img.shape[0]-2*k,img.shape[1]-2*k),np.uint8)
    for i in range (k, img.shape[0]-k):
        for j in range(k, img.shape[1]-k):
            isum=0
            for s in range(-k,k+1):
                isum += IBUF(img,i,j+s,n)
            back[i-k][j-k] = isum//(n**2)
    return back

def MedianSort(img,i,j,n):
    boxlist=[]
    for s in range (-n,n+1):
        for t in range (-n,n+1):
            boxlist.append(img[i+s][j+t])
    boxlist.sort()
    lens = len(boxlist)
    return(boxlist[(lens-1)//2])

def MedianFilterByN(img,n):
    k = (n-1)//2 #init point(k,k)
    back = np.zeros((img.shape[0]-2*k,img.shape[1]-2*k),np.uint8)
    for i in range (k, img.shape[0]-k):
        for j in range(k, img.shape[1]-k):
            back[i-k][j-k] = MedianSort(img,i,j,k)
    return back

def VS(Origin):
    sum=0
    n=Origin.shape[0]**2
    for i in range (Origin.shape[0]):
        for j in range(Origin.shape[1]):
            sum+=Origin[i][j]
    mean = sum/n
    var=0
    for i in range (Origin.shape[0]):
        for j in range(Origin.shape[1]):
            var+=((Origin[i][j]-mean)**2)
    vs=var/n
    return(vs)
def VN(Origin, Noise):#NoisePicture means the noise have been removed
    sum=0
    n=Origin.shape[0]**2
    for i in range (Origin.shape[0]):#Origin shape same as Noise
        for j in range(Origin.shape[1]):
            sum+=(int(Noise[i][j])-int(Origin[i][j]))
    mean_noise = sum/n
    var=0
    for i in range (Origin.shape[0]):
        for j in range(Origin.shape[1]):
            var+=((int(Noise[i][j])-int(Origin[i][j])-mean_noise)**2)
    vn=var/n
    return(vn)
def SNR(Origin,Noise):
    return (20*(math.log10(math.sqrt(VS(Origin))/math.sqrt(VN(Origin,Noise)))))

def main():
    img = cv2.imread('lena.bmp',0)
    kernel = [[-2, -1], [-2, 0], [-2, 1],
              [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
              [0, -2], [0, -1], [0, 0], [0, 1], [0, 2],
              [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
              [2, -1], [2, 0], [2, 1]]
    gs10 = GetGaussianNoise(img,10)
    print('GS10={:.3f}'.format(SNR(img,gs10)))
    gs30 = GetGaussianNoise(img,30)
    print('GS30={:.3f}'.format(SNR(img,gs30)))
    sp01 = GetSaltAndPepper(img,0.1)
    print('SP010={:.3f}'.format(SNR(img,sp01)))
    sp005= GetSaltAndPepper(img,0.05)
    print('SP005={:.3f}'.format(SNR(img,sp005)))
    # cv2.imwrite("GuassianNoise_10.png",gs10)
    # cv2.imwrite("GuassianNoise_30.png",gs30)
    # cv2.imwrite("SaltAndPepper010.png",sp01)
    # cv2.imwrite("SaltAndPepper005.png",sp005)
    # #Box-Filter3X3
    pd_gs10 =padding(gs10)
    pd_gs30 =padding(gs30)
    pd_sp01 =padding(sp01)
    pd_sp005 =padding(sp005)
    # bx33gs10=BoxFilterByN(pd_gs10,3)
    # bx33gs30=BoxFilterByN(pd_gs30,3)
    # bx33sp010=BoxFilterByN(pd_sp01,3)
    # bx33sp005=BoxFilterByN(pd_sp005,3)
    # print('box33_GS10={:.3f}'.format(SNR(img,bx33gs10 )))
    # print('box33_GS30={:.3f}'.format(SNR(img,bx33gs30)))
    # print('box33_SP010={:.3f}'.format(SNR(img,bx33sp010)))
    # print('box33_SP005={:.3f}'.format(SNR(img,bx33sp005)))
    # cv2.imwrite("box33_GS10.png",bx33gs10)
    # cv2.imwrite("box33_GS30.png",bx33gs30)
    # cv2.imwrite("box33_SP010.png",bx33sp010)
    # cv2.imwrite("box33_SP005.png",bx33sp005)
    # #Median-Filter3X3
    # md33gs10=MedianFilterByN(pd_gs10,3)
    # md33gs30=MedianFilterByN(pd_gs30,3)
    # md33sp010=MedianFilterByN(pd_sp01,3)
    # md33sp005=MedianFilterByN(pd_sp005,3)
    # print('md33_GS10={:.3f}'.format(SNR(img,md33gs10 )))
    # print('md33_GS30={:.3f}'.format(SNR(img,md33gs30)))
    # print('md33_SP010={:.3f}'.format(SNR(img,md33sp010)))
    # print('md33_SP005={:.3f}'.format(SNR(img,md33sp005)))
    # cv2.imwrite("md33_GS10.png",bx33gs10)
    # cv2.imwrite("md33_GS30.png",bx33gs30)
    # cv2.imwrite("md33_SP010.png",bx33sp010)
    # cv2.imwrite("md33_SP005.png",bx33sp005)
    # #Box-Filter5X5
    # pd_gs10 =padding(pd_gs10)
    # pd_gs30 =padding(pd_gs30)
    # pd_sp01 =padding(pd_sp01)
    # pd_sp005 =padding(pd_sp005)
    # bx55gs10=BoxFilterByN(pd_gs10,5)
    # bx55gs30=BoxFilterByN(pd_gs30,5)
    # bx55sp010=BoxFilterByN(pd_sp01,5)
    # bx55sp005=BoxFilterByN(pd_sp005,5)
    # print('box55_GS10={:.3f}'.format(SNR(img,bx55gs10 )))
    # print('box55_GS30={:.3f}'.format(SNR(img,bx55gs30)))
    # print('box55_SP010={:.3f}'.format(SNR(img,bx55sp010)))
    # print('box55_SP005={:.3f}'.format(SNR(img,bx55sp005)))
    # cv2.imwrite("box55_GS10.png",bx55gs10)
    # cv2.imwrite("box55_GS30.png",bx55gs30)
    # cv2.imwrite("box55_SP010.png",bx55sp010)
    # cv2.imwrite("box55_SP005.png",bx55sp005)
    # #Median-Filter5X5
    # md55gs10=MedianFilterByN(pd_gs10,5)
    # md55gs30=MedianFilterByN(pd_gs30,5)
    # md55sp010=MedianFilterByN(pd_sp01,5)
    # md55sp005=MedianFilterByN(pd_sp005,5)
    # print('md55_GS10={:.3f}'.format(SNR(img,md55gs10 )))
    # print('md55_GS30={:.3f}'.format(SNR(img,md55gs30)))
    # print('md55_SP010={:.3f}'.format(SNR(img,md55sp010)))
    # print('md55_SP005={:.3f}'.format(SNR(img,md55sp005)))
    # cv2.imwrite("md55_GS10.png",bx55gs10)
    # cv2.imwrite("md55_GS30.png",bx55gs30)
    # cv2.imwrite("md55_SP010.png",bx55sp010)
    # cv2.imwrite("md55_SP005.png",bx55sp005)
    
    # #opening-then-closing
    # opc_gs10=hw5.opening(gs10,kernel)
    # opc_gs10=hw5.closing(opc_gs10,kernel)
    # print('otc_gs10.png={:3f}'.format(SNR(img,opc_gs10)))
    # cv2.imwrite("otc_gs10.png",opc_gs10)
    # opc_gs30=hw5.opening(gs30,kernel)
    # opc_gs30=hw5.closing(opc_gs30,kernel)
    # print('otc_gs30.png={:3f}'.format(SNR(img,opc_gs30)))
    # cv2.imwrite("otc_gs30.png",opc_gs30)
    # opc_sp01=hw5.opening(sp01,kernel)
    # opc_sp01=hw5.closing(opc_sp01,kernel)
    # print('otc_sp01.png={:3f}'.format(SNR(img,opc_sp01)))
    # cv2.imwrite("otc_sp01.png",opc_sp01)
    # opc_sp005=hw5.opening(sp005,kernel)
    # opc_sp005=hw5.closing(opc_sp005,kernel)
    # print('otc_sp005.png={:3f}'.format(SNR(img,opc_sp005)))
    # cv2.imwrite("otc_sp005.png",opc_sp005)
    
    #closing-then-opening
    # cto_gs10=hw5.closing(gs10,kernel)
    # cto_gs10=hw5.opening(cto_gs10,kernel)
    # print('cto_gs10.png={:3f}'.format(SNR(img,cto_gs10)))
    # cv2.imwrite("cto_gs10.png",cto_gs10)
    # cto_gs30=hw5.closing(gs30,kernel)
    # cto_gs30=hw5.opening(cto_gs30,kernel)
    # print('cto_gs30.png={:3f}'.format(SNR(img,cto_gs30)))
    # cv2.imwrite("cto_gs30.png",cto_gs30)
    # cto_sp01=hw5.closing(sp01,kernel)
    # cto_sp01=hw5.opening(cto_sp01,kernel)
    # print('cto_sp01.png={:3f}'.format(SNR(img,cto_sp01)))
    # cv2.imwrite("cto_sp10.png",cto_sp01)
    # cto_sp005=hw5.closing(sp005,kernel)
    # cto_sp005=hw5.opening(cto_sp005,kernel)
    # print('cto_sp005.png={:3f}'.format(SNR(img,cto_sp005)))
    # cv2.imwrite("cto_sp005.png",cto_sp005)
    
    
    a=hw5.closing(pd_gs10,kernel)
    cto_gs10=hw5.opening(a,kernel)
    print('pdcto_gs10.png={:3f}'.format(SNR(img,cto_gs10)))
    cv2.imwrite('test.png',cto_gs10)

if __name__ == '__main__':
    main()
