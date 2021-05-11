import numpy as np
import cv2
import imutils
import math
import person

width = 600
height = width
PROXIMITY_THRESH = 90
CONTOUR_AREA_MIN = 10000
FRAME_BOUND_L = 0
FRAME_BOUND_R = width

# TODO: determine if customer is leaving frame 
def leaving_frame(x, y):
    return 1

# Calculate diff between previously stored person and possibly 
#  new object coordinates to determine if new person or not 
def prev_detect(x, y, person, pt):
    diff_x = abs(x - person.x)
    diff_y = abs(y - person.y)
    euclidean_dist = np.sqrt(np.square(diff_x) + np.square(diff_y)) 
    #return True if (diff_x <= pt and diff_y <= pt) else False
    return True if euclidean_dist <= 100 else False

if __name__ == "__main__":
    add_new_person = True 
    proximity_th = PROXIMITY_THRESH 
    people_arr = []
    cv2.startWindowThread()
    cap = cv2.VideoCapture(0)
    # TODO: figure our ratio for history, and varThreshold
    # - probably going to want high history since folks will be moving slow usually
    #fgbg = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=20)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    kernel_op = np.ones((3,3), np.uint8)
    kernel_cl = np.ones((10,10), np.uint8)

    while(True):
        ret, frame = cap.read()
        frame = imutils.resize(frame, width)
        # Setup screen 
        cv2.line(frame, (width // 2, 0), (width // 2, height), (250, 0, 1), 2)  # blue line
        cv2.line(frame, (width // 2 - 50, 0), (width // 2 - 50, height), (0, 0, 255), 2)  # red line
        # apply background subtractor to our frame
        fgmask = fgbg.apply(frame)
        # TODO: not sure if I like using threshold or not 
        #_, fgmask = cv2.threshold(fgmask, 254, 255, cv2.THRESH_BINARY)
        #cv2.imshow('frame', frame)
        cv2.imshow('fgmask', fgmask)
        # Erode->dilate pixels in frame using smaller kernel
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel_op)
        #cv2.imshow("opening", opening)
        # Dilate->erode pixels in frame using larger kernel
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_cl)
        #cv2.imshow("closing", closing)
        contours = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        for c in contours:
            if cv2.contourArea(c) < CONTOUR_AREA_MIN:
                continue
            add_new_person = True
            curr_person_id = 0
            # Get width, height, and starting loc of bound rectangle 
            (x, y, w, h) = cv2.boundingRect(c)
            mom_data = cv2.moments(c)
            centr_x = int(mom_data['m10'] / mom_data['m00'])
            centr_y = int(mom_data['m01'] / mom_data['m00'])
            # Is this a new person? (using proximity threshold)
            for p in people_arr:
                curr_person_id = p.id
                if prev_detect(centr_x, centr_y, p, proximity_th):
                    #update person file
                    p.update_loc(centr_x, centr_y)
                    add_new_person = False
            if add_new_person:
                curr_person_id += 1
                print("Added new person! ID: %s" % curr_person_id)
                new_person = person.Person(curr_person_id, centr_x, centr_y) 
                people_arr.append(new_person)    
            # Draw items around person
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            nametag = "ID " + str(people_arr[curr_person_id-1].id)
            cv2.putText(frame, nametag, (centr_x - 15,\
                centr_y - 10), cv2.FONT_HERSHEY_SIMPLEX,\
                0.5, (0,0,255), 2)
            cv2.circle(frame, (centr_x, centr_y), 1, (0, 0, 255), 5)
            center = (x + (w //2))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow("Security Feed", frame)

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

