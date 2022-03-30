#!/usr/bin/env python

import sys
import rospy
import cv2
import time
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

def main():
    global bridge
    pub = rospy.Publisher("/tennis_ball_image",Image,Queue_size=1)
    rospy.init_node("tennis_image_ball", anonymous=True)
    #video_capture = cv2.VideoCapture(0)
    video_capture = cv2.VideoCapture('/home/darsh/catkin_ws/src/ball_tracking/src/video/tennis-ball-video.mp4')


    #ret,frame = video_capture.read()

    #if ret:
    #    rospy.loginfo("Capturing Image Failed")

    rate = rospy.Rate(24)


    while (True):
        ret,frame = video_capture.read()
        #cv2.imshow("frame",frame)
        ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

        try:
            pub.publish(ros_image)
            rospy.loginfo("Publishing Image")            
        except CvBridgeError as e:
            print(e)
        rate.sleep()
        #if cv2.waitkey(1) & 0xFF == ord('q'):
        #    break

    #cv2.waitkey(0)
    #cv2.destroyAllwindows()    

if __name__ == '__main__':
    main()