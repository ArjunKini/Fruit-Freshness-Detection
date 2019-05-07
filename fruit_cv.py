from __future__ import division
import io
import os
import random
import cv2
import numpy as np
import time
from copy import deepcopy
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

# The name of the image file to annotate
i=time.strftime("%d-%m-%y_%H-%M-%S")

# capture image
camera = cv2.VideoCapture(0)
return_value, image = camera.read()
cv2.imwrite(i+'.jpeg', image)
del(camera)
frame=image
edge_img=deepcopy(image)
# finds edges in the input image image and
# marks them in the output map edges
edged = cv2.Canny(edge_img,50,100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
 
# find contours in the edge map
_,cnts, h = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

max_contA=cv2.contourArea(cnts[0])
max_cont=max(cnts,key=cv2.contourArea)

for i in range(len(cnts)):
    	x,y,w,h=cv2.boundingRect(max_cont)
    	cv2.rectangle(edge_img,(x,y),(x+w,y+h),(0,0,255), 2)
croppedk=frame[y:y+h,x:x+w]

# Display the fruit 
cv2.imshow('Edges',edge_img)

frame=edge_img

# converting BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     
# define range of red color in HSV
lower_red = np.array([0,50,50])
upper_red = np.array([10,255,255])
     
# create a red HSV colour boundary and 
# threshold HSV image
redmask1 = cv2.inRange(hsv, lower_red, upper_red)
    
# define range of red color in HSV
lower_red = np.array([170,50,50])
upper_red = np.array([180,255,255])
     
# create a red HSV colour boundary and 
# threshold HSV image
redmask2 = cv2.inRange(hsv, lower_red, upper_red)
 
redmask=redmask1+redmask2
maskOpen=cv2.morphologyEx(redmask,cv2.MORPH_OPEN,kernelOpen)
maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

maskFinal=maskClose
cv2.imshow('Red_Mask:',maskFinal)


cnt_r=0
for r in redmask:
	cnt_r=cnt_r+list(r).count(255)
print ("Redness ",cnt_r)

lower_green=np.array([50,50,50])
upper_green=np.array([70,255,255])
greenmask = cv2.inRange(hsv, lower_green, upper_green)
cv2.imshow('Green_Mask:',greenmask)
cnt_g=0
for g in greenmask:
	cnt_g=cnt_g+list(g).count(255)
print ("Greenness ",cnt_g)

lower_yellow=np.array([20,50,50])
upper_yellow=np.array([30,255,255])
yellowmask = cv2.inRange(hsv, lower_yellow, upper_yellow)
cv2.imshow('Yellow_Mask:',yellowmask)
cnt_y=0
for y in yellowmask:
	cnt_y=cnt_y+list(y).count(255)
print ("Yellowness ",cnt_y)


#Calculate ripeness
tot_area=cnt_r+cnt_y+cnt_g
rperc=cnt_r/tot_area
yperc=cnt_y/tot_area
gperc=cnt_g/tot_area


#Adjust the limits for your fruit
glimit=0.5
ylimit=0.8

if gperc>glimit:
	print ("Low Ripeness")
elif yperc>ylimit:
	print ("High Ripeness")
else:
	print ("Medium Ripeness")
# Wait for any key to close
while True: 
	k = cv2.waitKey(5) & 0xFF
	if k==27:
		break
# De-allocate any associated memory usage
cv2.waitKey(0)
cv2.destroyAllWindows() 




    
