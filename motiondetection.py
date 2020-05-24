# _*_ coding: utf-8 _*_
# _*_ coding: cp950 _*_

# author: Chi-Hsu Chen (css920@gmail.com)
# purpose: a simple python script for web cam test motion detection & direction detection
# datetime: 20200512

import sys
import cv2
import numpy as np

prevx=0
prevy=0

#function to show OpenCV version
def ShowOpenCVCurrentVersion():
    print(cv2.__version__)
    return

# find centroids
def findCentroids(contour,img):
    m=cv2.moments(contour)

    if m['m00'] != 0:
        x=int(m['m10']/m['m00'])
        y=int(m['m01']/m['m00'])

    cv2.circle(img,(x,y),3,(0,255,0),3)

    return x,y

# 使用absdiff偵測移動中的物體
def motionDetection(imgPrev,imgCurrent):
    # 先做灰階
    imgPrevGray=cv2.cvtColor(imgPrev,cv2.COLOR_BGR2GRAY)
    imgCurrentGray=cv2.cvtColor(imgCurrent,cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊
    imgPrevGaussianBlur=cv2.GaussianBlur(imgPrevGray,(5,5),0)
    imgCurrentGaussianBlur=cv2.GaussianBlur(imgCurrentGray,(5,5),0)

    # 差異處理
    imgDiff=cv2.absdiff(imgPrevGaussianBlur,imgCurrentGaussianBlur)

    # 差異影像二值化
    ret,imgBinary=cv2.threshold(imgDiff,10,255,cv2.THRESH_BINARY)

    # 先侵蝕再擴張以消除過多雜訊
    # 侵蝕處理
    imgErode=cv2.erode(imgBinary,None,iterations=2)
    # 擴張處理
    imgDilate=cv2.dilate(imgErode,None,iterations=10)

    # 抓取移動中物體輪廓
    contours,hierarchy=cv2.findContours(imgDilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # 此範例抓出最大的contour畫出
    if contours is None:
        return

    if len(contours)==0:
        return

    areas=[cv2.contourArea(contour) for contour in contours]
    contourAreaMaxIndex=np.argmax(areas)
    contourMax=contours[contourAreaMaxIndex]
    x,y,width,height=cv2.boundingRect(contourMax)
    cv2.rectangle(imgCurrent,(x,y),(x+width,y+height),(0,0,255),3)

    # 畫出重心
    centroidx,centroidy=findCentroids(contourMax,imgCurrent)

    global prevx,prevy   # 參考global變數
    if (prevx!=0) and (prevy!=0):
        cv2.line(imgCurrent,(prevx,prevy),(centroidx,centroidy),(0,0,255),2)
    
    # 決定移動方向
    (deltax,deltay)=(centroidx-prevx,centroidy-prevy)
    directionX=''
    directionY=''

    if deltax>10:
        directionX='LEFT'

    if deltax<-10:
        directionX='RIGHT'
    
    if deltay>10:
        directionY='DOWN'
    
    if deltay<-10:
        directionY='UP'

    print('deltax={} deltay={} directionX={} directionY{}'.format(deltax,deltay,directionX,directionY))
    cv2.putText(imgCurrent,'Motion direction:'+directionX+':'+directionY,(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0))

    prevx=centroidx
    prevy=centroidy

    ## 找前三大的area
    #sortedAreasIndex=np.argsort(areas)[::-1][:3]
    #top3AreaContours=[contours[index] for index in sortedAreasIndex]
    #
    #for c in top3AreaContours:
    #    x,y,width,height=cv2.boundingRect(c)
    #    cv2.rectangle(imgCurrent,(x,y),(x+width,y+height),(0,122,122),3)

    cv2.imshow('absdiff',imgDiff)
    cv2.imshow('binary absdiff',imgBinary)

# 測試使用網路攝影機web cam
def UseWebCam(camid):
    # 選擇第1隻攝影機
    cap = cv2.VideoCapture(camid)
    print('Frame default resolution: (' + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) + ';' + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) + ')')
    
    # 設定解析度
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while(True):
        ret, prevFrame = cap.read()
        # 從攝影機擷取一張影像
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        width=frame.shape[0]
        height=frame.shape[1]
        text='width=' + str(width) + 'height=' + str(height) +  'FPS:' + str(fps)
        
        # 偵測移動物體及方向
        motionDetection(prevFrame,frame)

        # 顯示圖片
        cv2.imshow('web cam test ' + text, frame)        
        # 若按下 q 鍵則離開迴圈
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放攝影機
    cap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()
    return

# main program
print('This is a OpenCV Test Python application. Press q if you want to exit...')
ShowOpenCVCurrentVersion()
camid=input('Select CamID (0 as default webcam, 1 as other additional USB webcam)')
if camid == '':
    camid=0
UseWebCam(camid)

