# pyMotionDetection
a simple python script for web cam test motion detection &amp; direction detection.

This script shows moving object tracking and finds the moving sequence of centroid within it. Then, the sequences are painted as lines to show the moving direction on screen. Also, text describing direction is attached on top of the moving object.  
Packages to install:
OpenCV, numpy  

===============================================  
這個script展示偵測移動物體追蹤，並且取其重心移動軌跡，以線條表示移動方向，並在移動物件方框上顯示移動方向  
所需安裝套件：
OpenCV, numpy

以下是此程式說法簡易說明：  
Step 1. 先從web cam上抓取分別在不同時間t1及t2的兩張畫面  
Step 2. 因為兩張畫面上除了移動部分外其他的畫素基本上是相同的，所以，我們只要根據這兩張畫面的差異就可以取出移動中物體的輪廓  
取出兩張圖的差異此處使用OpenCV的absdiff，結果如下圖左方:  
![image](https://github.com/ChiHsuChen/pyMotionDetection/blob/master/image/absdiff_and_originalimage.JPG)
Step 3. 最後使用OpenCV的findContours，針對absdiff產生結果找出輪廓，這時候就可以框出移動中物體

Demo on Youtube:  
[![Watch the video](https://img.youtube.com/vi/ESRatQ3SMPg/0.jpg)](https://www.youtube.com/watch?v=ESRatQ3SMPg)
