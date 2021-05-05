import argparse
import datetime
import imutils
import math
import cv2
import numpy as np
import csv

width = 600     # Camera width (x)
height = width 

body = 60        # used to set range of body boundary


blue= width/2 - 50    # location left boundary
red=width /2 +50  # location Right boundary
right = 0          # indicated whether the object triggered the right side first - meaning was heading out
left = 0

textOut = 0
textIn = 0

THRESHOLD_VAL = 80
CONTOUR_AREA_MIN = 15000
BACKGROUND_THRESH = 10


def writeCsv(str):
    outfile = open('test.csv', 'a')
    writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    #print(datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"))
    writer.writerow([str,datetime.datetime.now().strftime("%Y %B %d "),
                 datetime.datetime.now().strftime(" %I:%M:%S%p")])

    outfile.close()



# Possible ways to ignore background:
#  1. find all countors in background (first_image), keep in data struct
#  2. xor our all countors in bckground
#  3. once new object detected, keep all white pixels that are part of the object,
#	even if in same position as background contour 


if __name__ == "__main__":
    #camera = cv2.VideoCapture("test2.mp4")
    camera = cv2.VideoCapture(0)
    first_frame = None
    old_gray = 0
    first_frame_flag = 0

    
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break

        # resize the frame, convert it to grayscale, and blur (smooth) it
	# NOTE: based on the source code, imutils really only uses the width 
        frame = imutils.resize(frame, width)
	# First convert to grayscale to reduce complexity
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# Then, blur (smooth) the image to eliminate noise
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
	#cv2.imshow("Gray Blur", gray)

        # if the first frame is None, initialize it
        if first_frame is None:
            first_frame = gray
            #continue

        # compute the absolute difference between the current frame and
        # first frame
        #frameDelta = cv2.absdiff(old_gray, gray)
	# if this frame isn't background, OR our new frame on the background
	#thresh = cv2.threshold(frameDelta, THRESHOLD_VAL, 255, cv2.THRESH_BINARY_INV)[1]

	# Put dark objects to white, light to black, use current image 
	thresh = cv2.threshold(gray, THRESHOLD_VAL, 255, cv2.THRESH_BINARY_INV)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
	# This function looks for contours of white 
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        
	# grab previous frame
	old_gray = gray

	# Setup screen 
	cv2.line(frame, (width // 2, 0), (width // 2, height), (250, 0, 1), 2)  # blue line
	cv2.line(frame, (width // 2 - 50, 0), (width //2 - 50, height), (0, 0, 255), 2)  # red line

        # loop over the contours
        for c in cnts:
            #print(c)
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < CONTOUR_AREA_MIN:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


            rectangleCenterPoint = ( x +( w // 2), y +( h // 2))
	    cv2.putText(frame, "HANDSOME MAN", (rectangleCenterPoint[0] - 15,\
			rectangleCenterPoint[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,\
		        0.5, (0,0,255), 2)
            cv2.circle(frame, rectangleCenterPoint, 1, (0, 0, 255), 5)
            center = (x + (w //2))
            if (center - body) < blue and (center + body) >blue:
                if right == 1:
                   textOut += 1
                   right = 0
                   #writeCsv('out')
                else:
                   left =1
            if (center - body) < red and (center + body) >red:
                if left == 1:
                   textIn += 1
                   left = 0
                   #writeCsv('in')
                else:
                   right =1        

            # draw the text and timestamp on the frame


            # show the frame and record if the user presses a key
            #cv2.imshow("Thresh", thresh)
            #cv2.imshow("Frame Delta", frameDelta)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.putText(frame, "In: {}".format(str(textIn)), (10, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Out: {}".format(str(textOut)), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                   (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Thresh", thresh)
        #cv2.imshow("First_Thresh", first_thresh)
        #cv2.imshow("Curr_Thresh", curr_thresh)
	cv2.imshow("Security Feed", frame)

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
