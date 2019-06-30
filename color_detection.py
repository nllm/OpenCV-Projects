#!/usr/bin/python
import cv2
import numpy as np

vcap = cv2.VideoCapture(0)

while(1):

    # Tomamos el cuadro con la cámara
    _, frame = vcap.read()

    # Convertimos BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

    # definimos los rangos de colores
    lower_red = np.array([-15,150,150])
    upper_red = np.array([10,255,255])
    lower_yellow = np.array([20,200,200])
    upper_yellow = np.array([30,255,255])

    # Se obtienen solo los colores que definimos
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #se suman las dos máscaras para tenerlas en una sola pantalla
    mask= mask_red+mask_yellow    

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Aqui mostramos la imagen en blanco o negro segun el rango de colores.
    bn_imgred = cv2.inRange(hsv, lower_red, upper_red)
    bn_imgyellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #se suman los filtros para tenerlos en una sola imagen
    bn_img= bn_imgred+bn_imgyellow
 
    # Limpiamos la imagen de imperfecciones con los filtros erode y dilate
    bn_img = cv2.erode (bn_img,cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)),iterations = 1)
    bn_img = cv2.dilate (bn_img,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)),iterations = 1)
    # Localizamos la posicion del objeto rojo
    M = cv2.moments(bn_imgred)
    if M['m00']>50000:
        rx = int(M['m10']/M['m00'])
        ry = int(M['m01']/M['m00'])
    # Localizamos la posicion del objeto amarillo
    M = cv2.moments(bn_imgyellow)
    if M['m00']>50000:
        yx = int(M['m10']/M['m00'])
        yy = int(M['m01']/M['m00'])
    # Mostramos un circulo verde en la posicion en la que se encuentra el objeto rojo
        cv2.circle (frame,(rx,ry),20,(0,255,0), 2)
    #Mostramos un circulo azul en la posicion en la que se encuentra el objeto amarillo
        cv2.circle (frame,(yx,yy),20,(255,255,0), 2)    
 
    # Creamos las ventanas de salida 
    cv2.imshow('Salida', frame)
    cv2.imshow('inRange', bn_img)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
