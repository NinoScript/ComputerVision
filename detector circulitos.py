#!/usr/bin/python
# -*- coding: utf-8 -*-
# Detector de Circulitos, por Cristián Arenas Ulloa (licencia CC BY-SA 3.0)
import cv2

# algunos parámetros para modificar:
hsv_desde = ( 30,  50,  80) # inicio rango de colores
hsv_hasta = ( 70, 255, 255) # fin rango de colores
se_size = (7, 7) # elemento estructurante para morfología
min_dist = 80 # distancia mínima entre círculos
rad_min = 50 # radio mínimo, si es cero no hay mínimo
rad_max = 0 # radio máximo, si es cero no hay máximo
frame_interval = 20 # inverso del framerate
color_circulo = (0, 100, 255) # cómo los marcamos en la pantalla
gaussian_power = 11 # cuanto blur gaussiano le metemos

# funciones convenientes:
def waitAndProcessEvents():
	# el waitKey este es necesario para que opencv lea los eventos
	# si lo sacamos, no se puede conectar bien a las cámaras
	cv2.waitKey(frame_interval)

# hacemos las ventanitas
window_camara   = "camara con circulos"
window_preHough = "imagen que entra a hough"
cv2.namedWindow(window_camara)
cv2.namedWindow(window_preHough)
cv2.moveWindow(window_preHough, 600, 0)

# nos conectamos a la cámara
capture = cv2.VideoCapture(0)
if not capture:
	print("Could not open webcam")
	sys.exit(1)

while True:
	# intentamos leer una imagen
	ret, img = capture.read()
	if img == None:
		waitAndProcessEvents()
		continue
	# si llegamos aquí, entonces tenemos imagen
	
	# pasamos la imagen a HSV para filtrar por color
	hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	thresholded = cv2.inRange(hsv_frame, hsv_desde, hsv_hasta)
	
	# hacemos un poco de morfología pa borrar basura
	se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, se_size)
	thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN,  se)
	thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, se)
	
	# suavisamos un poco la imagen para que le sea más fácil encontrar círculos
	thresholded = cv2.GaussianBlur(thresholded, (0, 0), gaussian_power)
	
	
	# mostramos la imagen que le vamos a meter al algoritmo de los dibujitos
	# así nos aseguramos de que estamos filtrando bien
	cv2.imshow("imagen que entra a hough", thresholded)
	
	# encontramos los circulitos
	circles = cv2.HoughCircles(thresholded, cv2.cv.CV_HOUGH_GRADIENT, 1,
	                           min_dist, param1=50, param2=30,
	                           minRadius=rad_min, maxRadius=rad_max)
	
	# si no hay circulitos, no hacemos nada más
	if circles == None:
		waitAndProcessEvents()
		continue
	#si llegamos aquí es porque hay circulitos
	
	# dibujar cada circulito encontrado
	for i in circles[0,:]: #circles[0] ?
		center = (i[0],i[1])
		radius = i[2]
		cv2.circle(img, center, radius, color_circulo, 2)
	
	# mostramos la imagen con los círculos dibujados
	cv2.imshow(window_camara, img)
	
	# limitamos el framerate y seguimos con el loop
	waitAndProcessEvents()

# This work by Cristián Arenas Ulloa is licensed under a
# Creative Commons Attribution-ShareAlike 3.0 Unported License.
# Based on a work at https://github.com/NinoScript/ComputerVision.
# To view a copy of this license, visit
# http://creativecommons.org/licenses/by-sa/3.0/deed.en_US.