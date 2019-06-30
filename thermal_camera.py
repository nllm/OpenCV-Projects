#use of a camera to create a thermal image

import numpy as np
import cv2
import time
from pylepton import Lepton
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)



#Normalizar temperatura
with Lepton() as l:
 
    a,_ = l.capture()
    cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
    np.right_shift(a, 8, a) # fit data into 8 bits
    cv2.imwrite("output.jpg", np.uint8(a)) # write it!

img=cv2.imread('output.jpg', 0)
img2=cv2.imread('output.jpg')
height, width=img.shape
minval, maxval, minloc, maxloc = cv2.minMaxLoc(img)

print(minloc)
print(maxloc)
print(height, width)

#tempref=raw_input('Reference temp:')

xmin, ymin = minloc
xmax, ymax= maxloc

#cv2.circle(img2, (xmin, ymin), 5, (255,0,0), 2)
#cv2.circle(img2, (xmax, ymax), 5, (0,0,255), 2)
#cv2.imshow('Termo', img2)
#prom=(minval+maxval)/2
#temp=(prom/prom)*float(tempref)
temp=21.1
cv2.waitKey(0)
cv2.destroyAllWindows()
i=0
while (1):

    with Lepton() as l:
 
        a,_ = l.capture()
        cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
        np.right_shift(a, 8, a) # fit data into 8 bits
        cv2.imwrite("output%i.jpg" %i, np.uint8(a)) # write it!
        
    img=cv2.imread('output%i.jpg' %i, 0)
    img2=cv2.imread('output%i.jpg' %i)
    res=cv2.resize(img, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
    height, width=img.shape
    rgb=cv2.applyColorMap(res, cv2.COLORMAP_HOT)
    minval, maxval, minloc, maxloc = cv2.minMaxLoc(img)
    cv2.rectangle(rgb, (10, 10), (40, 410), (255, 255, 255), 2)

    roi=img[0:20,0:350]
    minvalr, maxvalr, minlocr, maxlocr = cv2.minMaxLoc(roi)
    prom2=(maxvalr+minvalr)/2
    print(prom2)
    y2=int((prom2/30)*40)
    
    b=0
    g=0
    r=0
    y=410
    while(r<255):
        r=r+1.5
        y=y-1
        cv2.rectangle(rgb, (12, y), (38, y-2), (b, g, r), 1)
    g=0
    b=0
    while(y>12):        
        b=b+1.2
        g=g+2
        y=y-1
        cv2.rectangle(rgb, (12, y), (38, y-2), (b, g, r), 1)
    input_state = GPIO.input(23)
    if input_state == False:
        print('Button pressed')
        i=i+1
        
    font=cv2.FONT_HERSHEY_PLAIN
    cv2.putText(rgb,str(temp-17.5),  (42,560-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp-14),  (42,520-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp-10.5),  (42,480-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp-7.0),  (42, 440-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp-3.5),  (42,400-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp),  (42,360-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp+3.5),  (42,320-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp+7),  (42,280-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp+10.5),  (42,240-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp+14),  (42,200-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp+17.5),  (42,160-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp+21),  (42,120-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp+24.5),  (42,80-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp+28),  (42,40-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    cv2.putText(rgb,str(temp+31.5),  (42,0-y2), font, 1, (255, 255, 255),2,cv2.CV_AA)
    #cv2.rectangle(rgb, (0,10), (20, 400), (255, 0, 0), 1)
    cv2.imshow('Termo', rgb)
  
    cv2.waitKey(1)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
    #cv2.destroyAllWindows()
    #cv2.waitKey(0)
   
   

