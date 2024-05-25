import cv2
import numpy as np
lineHeight=550
#穿过直线的车的数量
Car_nums=0
#储存中心坐标的数组
cars=[]
#KNN算法去背景
removebg=cv2.createBackgroundSubtractorKNN()
def center(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    33
    return cx,cy
 
video=cv2.VideoCapture('video.mp4')
 
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
 
while True:
    ret,frame=video.read()
    if(ret!=0):
        #灰度
        cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #高斯去噪
        blur=cv2.GaussianBlur(frame,(5,5),5)
        mask=removebg.apply(blur)
        
        #腐蚀
        erode=cv2.erode(mask,kernel,iterations=2)#iteration=n 迭代n次
        #膨胀
        dilate=cv2.dilate(erode,kernel,iterations=2)
        #cv2.imshow("x",dilate)
        dst=cv2.morphologyEx(dilate,cv2.MORPH_CLOSE,kernel)
        #cv2.imshow("x1",dst)
                          
        #画出检测线
        cv2.line(frame,(10,lineHeight),(1400,lineHeight),(255,0,0),2)
        counts,h=cv2.findContours(dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #遍历所有轮廓
        for(i,c) in enumerate(counts):
            (x,y,w,h)=cv2.boundingRect(c)
            
            if((w<=90) and (h<=90)):
                continue
            if(y<66):
                continue
            #将有效的车绘制出来
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cpoint=center(x,y,w,h)
            cars.append(cpoint)#将中心点储存到cars数组中
            
            for (x,y) in cars:
                if(y>lineHeight-7 and y<lineHeight+7):
                    Car_nums +=1
                    cars.remove((x,y))
                    print(Car_nums)
        
        cv2.putText(frame,"Cars nums:"+str(Car_nums),(500,60),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0))
        cv2.imshow("video",frame)
        
    key=cv2.waitKey(1)
    if(key==27):
        break
 
video.release()
cv2.destroyAllWindows()        