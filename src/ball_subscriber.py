#!/usr/bin/env python

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from ball_detection_final import *


def image_callback(ros_image):
    global bridge
    try:
        cv_image = bridge.imgmsg_to_cv2(ros_image, "bgr8")
    except CvBridgeError as e:
        print(e)


    cv2.imshow("Image window", cv_image)
    YellowLower = (30,150,100)
    YellowUpper = (50,255,255)
    rgb_image = cv_image
    binary_image_mask = filter_color(rgb_image,YellowLower,YellowUpper)
    contours = getContours(binary_image_mask)
    draw_ball(binary_image_mask,rgb_image,contours)  
    cv2.waitKey(3)


def main(args):
  rospy.init_node('image_subscriber', anonymous=True)

  image_sub = rospy.Subscriber("/tennis_ball_image",Image,image_callback)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)