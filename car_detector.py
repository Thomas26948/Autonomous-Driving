import cv2
import numpy as np
import argparse
import time
import os

def main():
	pass

# python3 car_detector.py --video Ressources/test.mp4 --length 20 --write result.mp4
# si on write on ne voit pas le résultat en même temps que le calcul

# Origine : en haut à gauche avec y croit vers le bas et x vers la droite
# Image : (x,y) le sommet en haut à gauche de chaque cadre à partir de l'origine de l'image
# Video : (x,y) le sommet en haut à gauche de chaque cadre à partir de region of Intrest

if __name__ == '__main__' :
	parser = argparse.ArgumentParser(description='Script to run haarcascade detection method')
	parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
	parser.add_argument("--write", help="Write output to file")
	parser.add_argument("--length", type=int, default=20, help="Max processing time in second for video output, default is 20 seconds")
	args = parser.parse_args()

	car_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__)) + '/cars.xml')

	if args.video :
				cap = cv2.VideoCapture(args.video)
				nFrames = int(cap.get(7))
				pseudoWidth = int(cap.get(3))
				pseudoHeight = int(cap.get(4))
				fps = cap.get(5)
				bShouldContinue = True
				counter = 30 * args.length

				if args.write :
					fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
					out = cv2.VideoWriter(args.write, fourcc, 30.0, (pseudoWidth,pseudoHeight)) #must be the exact same resolution for MJPG ENCODING

				while counter > 0 :

						if cap.isOpened() :
								ret, frame = cap.read()

								if not ret :
										bShouldContinue = False
										break

								width, heigth = frame.shape[1], frame.shape[0]
								xroi, yroi, wroi, hroi = 5*heigth/12, width/12, 11*heigth/12, 11*width/12
								xroi, yroi, wroi, hroi = int(xroi), int(yroi), int(wroi), int(hroi)
								roi = frame[xroi:wroi, yroi:hroi]

								cv2.putText(frame, "Region of interest", (yroi,xroi-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
								cv2.rectangle(frame, (yroi,xroi),(hroi,wroi),(255,255,255),1)

								gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
								cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(70, 70))

								print("This Frame")
								print("**********")
								i=1
								for (x,y,w,h) in cars :
										cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),4)
										print("Car ",i)
										print("x : ",x)
										print("y :",y)
										print()
										i+=1


								if args.write :
									out.write(frame)
								else :
									cv2.imshow('Cars processed', frame)
									cv2.waitKey(int(1/fps*1000))
								counter -= 1

	else :
				img = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '/Ressources' + '/1.png');
				print(os.path.dirname(os.path.realpath(__file__)) + '/Ressources' + '/1.png')
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

				print(cars)

				i=1
				for (x,y,w,h) in cars :
						cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),4)
						print("Car ",i)
						print("x : ",x)
						print("y :",y)
						print()
						i+=1


				cv2.imshow('Cars processed', img)

				if cv2.waitKey() >= 0:
					bShouldContinue = False

cv2.destroyAllWindows()

