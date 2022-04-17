from pyfirmata import Arduino,SERVO
from time import sleep
import cv2
import numpy as np

port='COM6'
pin=10
board=Arduino(port)
board.digital[pin].mode=SERVO

def nothing(x):
          pass

def rotate(pin,angle):
          board.digital[pin].write(angle)
          #sleep(.15)

cap=cv2.VideoCapture(0)
kernel=np.ones((1,1),np.uint8)
background_sub=cv2.createBackgroundSubtractorMOG2(history=120)

while True:
          
          t=False
          _,frame=cap.read()
          roi=frame[140:320,230:410]
          #blur=cv2.GaussianBlur(frame,(3,3),0,borderType=cv2.BORDER_CONSTANT)
          hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)#hsv can actually control the conc (brightness) of the colors
                    
          lower=np.array([60,0,185])
          upper=np.array([160,255,255])#the max values that the hsv takes first one is for the color second one is for greyness and third is for brightness

          mask=cv2.inRange(hsv,lower,upper)
          #dil=cv2.dilate(mask,kernel)
          thresh=background_sub.apply(mask)
          result=cv2.bitwise_and(roi,roi,mask=mask)

          contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
          for c in contours:
                    area=cv2.contourArea(c)
                    if area > 1000:
                              #cv2.drawContours(frame,[c],-1,(0,255,0),2)
                              x,y,w,h=cv2.boundingRect(c)
                              cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),2)
                              t=True
                            
          cv2.imshow('frame',frame)
          cv2.imshow('mask_hsv',mask)
          cv2.imshow('result',result)
          cv2.imshow('adavanced mask',thresh)

          while t:
                    rotate(pin,90)
                    break
          while not t:
                    rotate(pin,0)
                    break
                   
          
          key=cv2.waitKey(1)
          if key==27:
                    break
                    
cap.release()
cv2.destroyAllWindows()
