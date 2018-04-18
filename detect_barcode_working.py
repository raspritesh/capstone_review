# USAGE
# python detect_barcode.py --image images/barcode_01.jpg

# import the necessary packages
import numpy as np
import argparse
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path")
args = vars(ap.parse_args())

# load the image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# compute the Scharr gradient magnitude representation of the images
# in both the x and y direction
gradX = cv2.Sobel(gray, ddepth = cv2.cv.CV_32F, dx = 1, dy = 0, ksize = -1)
gradY = cv2.Sobel(gray, ddepth = cv2.cv.CV_32F, dx = 0, dy = 1, ksize = -1)

# subtract the y-gradient from the x-gradient
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

# blur and threshold the image
blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

# construct a closing kernel and apply it to the thresholded image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# perform a series of erosions and dilations
closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)

# find the contours in the thresholded image, then sort the contours
# by their area, keeping only the largest one
(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
print c[0]
print c[1]
[x,y,w,h] = cv2.boundingRect(c)
print x,y,w,h
#x,y,w,h = cv2.boundingRect(c)
#img = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
img=image[x-40:y+h+10,y:x+w+20]
#cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
cv2.imshow("Image1",img)
cv2.imwrite( "/home/pi/Downloads/img1.jpg", img );
[a]=decode(Image.open("/home/pi/Downloads/img1.jpg"))
print a[0]
#img=image[x:y,x+w:y+h]
#cv2.imshow("Image3",img)
#mask = np.zeros_like(image) # Create mask where white is what we want, black otherwise
#out = np.zeros_like(image) # Extract out the object and place into output image
#out[mask == 255] = image[mask == 255]

# Now crop
#(x, y) = np.where(mask == 255);
#(topx, topy) = (np.min(x), np.min(y));
#(bottomx, bottomy) = (np.max(x), np.max(y));
#out = out[topx:bottomx+1, topy:bottomy+1];

# Show the output image
#cv2.imshow('Output', out)

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
#print rect
box = np.int0(cv2.cv.BoxPoints(rect))
print  box
#print box[0]
#print box[1]
#print box[2]
#print box[3]
#lu=image[126:339,274:363]
#cv2.imshow("Image2",lu)
# draw a bounding box arounded the detected barcode and display the
# image
#print box.shape
cv2.drawContours(image, [box], -1, (255, 255, 0), 1)

cv2.imshow("Image", image)
cv2.waitKey(0)
