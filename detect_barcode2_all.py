# USAGE
#linked to mysql
#tested-working good -11/03/2018
#before running create database using insert commmands
#insert into e(id,name,bookid,bookname,issuedate,returndate,status)values("14BEC0***","652837659","9781904994862",
#                                                                         "dip","22/07/2017","15/08/2017","1");
#insert into e(id,name,bookid,bookname,issuedate,returndate,status)values("14BEC0***","qwertyu","005150024163",
#                                                                         "dip","22/12/2017","15/01/2018","1");

#set date properly by following command
#sudo date -s"Mon aug 12 20:14:11 UTC 2014"

# python detect_barcode.py --image images/barcode_01.jpg

# import the necessary packages
import timeit
import numpy as np
import argparse
import cv2
import time
from datetime import date
from pyzbar.pyzbar import decode
from PIL import Image
import MySQLdb as m
import serial
import types
def fine(d1,m1,y1,d2,m2,y2):
    a=0
    d=date(y1,m1,d1)
    e=date(y2,m2,d2)
    delta=e-d
    a=delta.days
    return a


start_time= timeit.default_timer()
db=m.connect("localhost","root","ritesh","cap")
import RPi.GPIO as gpio
sql="""CREATE TABLE IF NOT EXISTS e(id varchar(50) not null)"""
cur=db.cursor()
cur.execute(sql)
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path")
args = vars(ap.parse_args())

# load the image and convert it to grayscale
image = cv2.imread(args["image"])
if image== None:
	print "yes"
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
#print "gbwiehg"
# perform a series of erosions and dilations
closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)

# find the contours in the thresholded image, then sort the contours
# by their area, keeping only the largest one
(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
[x,y,w,h] = cv2.boundingRect(c)
#x,y,w,h = cv2.boundingRect(c)
#img = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
img=image[x-5:y+h-5,y+5:x+w+5]
#cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
cv2.imshow("Image1",img)
cv2.imwrite( "/home/pi/Downloads/img1.jpg", img );
[a]=decode(Image.open("/home/pi/Downloads/img1.jpg"))
#print a[0]
#img=image[x:y,x+w:y+h]
#cv2.imshow("Image3",img)
#mask = np.zeros_like(image) # Create mask where white is what we want, black otherwise
#out = np.zeros_like(image) # Extract out the object and place into output image
#out[mask == 255] = image[mask == 255]
#print "bdhg"
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
#print  box
#print box[0]
#print box[1]
#print box[2]
#print box[3]
#lu=image[126:339,274:363]
#cv2.imshow("Image2",lu)
# draw a bounding box arounded the detected barcode and display the
# image
#print box.shape
cv2.drawContours(image, [box], -1, (255, 255, 0), 3)

#cv2.imshow("Image", image)
#print a[0]
sql="select id,name,bookname,issuedate,returndate from e where bookid='%s' and status='1';" %a[0]
cur.execute(sql)
result=cur.fetchall()
if result==():
        print "None"
else:
        for row in result:
                Id=row[0]
                name=row[1]
                bookname=row[2]
                issuedate=row[3]
                returndate=row[4]
        print "Registration Number='%s'"%Id,
        print "Name='%s'"%name,
        print "Book Name='%s'"%bookname
        q=1
	l=[]
        l=returndate.split('/')
        now=time.strftime("%d/%m/%Y")
	k=[]
        k=now.split("/")
        j=map(int,k)
        p=map(int,l)
        g=fine(p[0],p[1],p[2],j[0],j[1],j[2])
     
        if g<0:
                g=0
        print "Fine=Rs.%s"%g
        sql="update e set status='0' where bookid='%s';"%a[0]
try:
                	
    cur.execute(sql)
    db.commit()
			
except Exception as e:
    print "Some error occured:",e
    db.rollback()
elapsed=timeit.default_timer()-start_time
print elapsed



        

