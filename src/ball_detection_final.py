#!/usr/bin/env python

from tkinter import image_names
from matplotlib.pyplot import contour
import numpy as np
import cv2

def rgb_image_read(image,show):
    rgb_image = cv2.imread(image)
    if show:
        cv2.imshow("RGB Image", rgb_image)
    return rgb_image

def filter_color(rgb_image, Lower_bound, Upper_bound):
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV Image", hsv_image)

    YellowLower = (30,150,100)
    YellowUpper = (50,255,255)

    mask = cv2.inRange(hsv_image, Lower_bound, Upper_bound)

    return mask

def getContours(binary_image):
    contours, hierarchy = cv2.findContours(binary_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_ball(binary_image, rgb_image, contours):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')

    for c in contours:
        area = cv2.contourArea(c)
        perimeter= cv2.arcLength(c, True)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if (area>15000):
            cv2.drawContours(rgb_image, [c], -1, (150,250,150), 1)
            cv2.drawContours(black_image, [c], -1, (150,250,150), 1)
            cx, cy = contour_center(c)
            cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(black_image, (cx,cy),5,(150,150,255),-1)
            print ("Area: {}, Perimeter: {}".format(area, perimeter))
    print ("number of contours: {}".format(len(contours)))
    cv2.imshow("RGB Image Contours",rgb_image)
    cv2.imshow("Black Image Contours",black_image)

def contour_center(contour):
    M = cv2.moments(contour)
    cx=-1
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    return cx, cy

def main():
    image_name = "/home/darsh/catkin1_ws/src/ros_essentials_cpp/src/topic03_perception/images/tennisball04.jpg"
    YellowLower = (30,150,100)
    YellowUpper = (50,255,255)
    rgb_image = rgb_image_read(image_name,True)
    binary_image_mask = filter_color(rgb_image,YellowLower,YellowUpper)
    contours = getContours(binary_image_mask)
    draw_ball(binary_image_mask,rgb_image,contours)
    
    #video_capture = cv2.VideoCapture(0)
    #video_capture = cv2.VideoCapture('video/tennis-ball-video.mp4')
    
    #while(True):
     #   ret, frame = video_capture.read()
      #  detect_ball_in_a_frame(frame)
       # time.sleep(0.033)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   break

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

cv2.waitKey(0)
cv2.destroyAllWindows()