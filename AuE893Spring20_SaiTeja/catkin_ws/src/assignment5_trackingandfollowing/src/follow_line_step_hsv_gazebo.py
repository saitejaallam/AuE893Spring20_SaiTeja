#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from move_robot import MoveTurtlebot3


class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.moveTurtlebot3_object = MoveTurtlebot3()
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        self.twist_object = Twist()


    def camera_callback(self,data):

	# We select bgr8 because its the OpneCV encoding by default
	cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
    
            
        # We get image dimensions and crop the parts of the image we dont need
        height, width, channels = cv_image.shape

        # Crop the primary mask image to be very small
        crop_img = cv_image[(height)/2+100:(height)/2+120][1:width]

        # Crop the secondary mask image to be much larger 
        crop_img2 = cv_image[1:300][1:width]

        # Note: A primary mask and a secondary mask are used so when there is no 
        # yellow line found within the primary mask (a small window), then the 
        # secondary mask is used (a much larger window)
        
        # Convert from RGB to HSV for both images
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2HSV)
        
        # Define the Yellow Colour in HSV

        """
        To know which color to track in HSV use ColorZilla to get the color registered by the camera 
        in BGR and convert to HSV. 
        """

        # Threshold both of the HSV images to get only yellow colors
        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([50,255,255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask2 = cv2.inRange(hsv2, lower_yellow, upper_yellow)
        
        # Calculate centroid of the blob of binary image using ImageMoments for both images
        m = cv2.moments(mask, False)
        m2 = cv2.moments(mask2, False)

        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cx, cy = height/2, width/2

        try:
            cx2, cy2 = m2['m10']/m2['m00'], m2['m01']/m2['m00']
        except ZeroDivisionError:
            cx2, cy2 = height/2, width/2
        
        # Draw the centroid in the resultut images
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) 
        cv2.circle(mask,(int(cx), int(cy)), 10,(0,0,255),-1)
        cv2.circle(mask2,(int(cx2), int(cy2)), 10,(0,0,255),-1)

        # Determine the error of the centroid with the middle of the image for 
        # both images
        err = cx - width/2
        err2 = cx2 - width/2

        # Determine if no yellow is seen in the primary mask image, if not, then 
        # check the secondary image. 
        # Else there is yellow and move towards it/follow it. 
        allZero = not np.any(mask)
        if allZero == 1:

            # Determine if no yellow is seen in the secondary mask image, if not, 
            # then do not move linearly and just turn to try an find yellow lines.
            # Else there is yellow, then move towards it. 
            allZero2 = not np.any(mask2)
            if allZero2 == 1:
                self.twist_object.angular.z = 0.5
                self.twist_object.linear.x = 0
                #print("all zero, NO big picture, TURN")
            else:
                self.twist_object.angular.z = -float(err2) / 100
                self.twist_object.linear.x = 0.4
                #print("all zero, big picture")

        else:
            self.twist_object.linear.x = 0.4
            self.twist_object.angular.z = -float(err) / 100

        # Publish the command
        self.cmd_vel_pub.publish(self.twist_object)

        # Print the camera image, no changes
        cv2.imshow("Original", cv_image)
        # Print the primary mask image
        cv2.imshow("Primary Mask", mask)
        # Print the secondary mask image
        cv2.imshow("Secondary Mask", mask2)
        cv2.waitKey(3)
        
        
    def clean_up(self):
        self.moveTurtlebot3_object.clean_class()
        cv2.destroyAllWindows()
        
        

def main():
    rospy.init_node('line_following_node', anonymous=True)
    
    
    line_follower_object = LineFollower()

    
    rate = rospy.Rate(5)
    ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        line_follower_object.clean_up()
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        rate.sleep()

    
    
if __name__ == '__main__':
    main()
