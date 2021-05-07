import numpy as np
import cv2
import imutils
import math
import person

width = 600
height = width
CONTOUR_AREA_MIN = 10000

if __name__ == "__main__":
    add_new_person = False
    cv2.startWindowThread()
    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    kernel_op = np.ones((3,3), np.uint8)
    kernel_cl = np.ones((10,10), np.uint8)

    while(True):
        ret, frame = cap.read()
        frame = imutils.resize(frame, width)
        # Setup screen 
        cv2.line(frame, (width // 2, 0), (width // 2, height), (250, 0, 1), 2)  # blue line
        cv2.line(frame, (width // 2 - 50, 0), (width //2 - 50, height), (0, 0, 255), 2)  # red line
        # apply background subtractor to our frame
        fgmask = fgbg.apply(frame)
        #cv2.imshow('frame', frame)
        cv2.imshow('fgmask', fgmask)
        # Erode->dilate pixels in frame using smaller kernel
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel_op)
        #cv2.imshow("opening", opening)
        # Dilate->erode pixels in frame using larger kernel
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_cl)
        #cv2.imshow("closing", closing)
        cntrs = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        for c in cntrs:
            if cv2.contourArea(c) < CONTOUR_AREA_MIN:
                continue
            # Get wid, height, and center loc of contour
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rectangleCenterPoint = ( x +( w // 2), y +( h // 2))
            cv2.putText(frame, "CUSTOMER", (rectangleCenterPoint[0] - 15,\
                rectangleCenterPoint[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,\
                0.5, (0,0,255), 2)
            cv2.circle(frame, rectangleCenterPoint, 1, (0, 0, 255), 5)
            center = (x + (w //2))
            # Tracking content goes here

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow("Security Feed", frame)

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

