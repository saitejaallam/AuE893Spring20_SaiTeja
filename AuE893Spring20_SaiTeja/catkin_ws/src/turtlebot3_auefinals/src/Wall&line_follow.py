#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image, LaserScan
from move_robot import MoveTurtlebot3
from math import sqrt,pow,atan2
#from wall_follow import AvoidObstacles

line_confirm = False
right_dist = 0
left_dist = 0
front_dist= 0


class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.moveTurtlebot3_object = MoveTurtlebot3()

    def camera_callback(self,data):
        # We select bgr8 because its the OpneCV encoding by default
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)    
            
        # We get image dimensions and crop the parts of the image we dont need
        height, width, channels = cv_image.shape

        descentre = 220
        rows_to_watch = 20

        # Crop the primary mask image to be very small
        #crop_img = cv_image[(height)/2+descentre:(height)/2+(descentre+rows_to_watch)][1:width]
	crop_img = cv_image[(height)/2:(height)/2+(descentre+rows_to_watch)][1:width]
        #showimg = cv_image[(height)/2+100:(height)/2+120][1:width]

        # Convert from RGB to HSV for both images
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
       
        # Define the Yellow Colour in HSV

        """
        To know which color to track in HSV use ColorZilla to get the color registered by the camera 
        in BGR and convert to HSV. 
        """

        # Threshold both of the HSV images to get only yellow colors
        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([50,255,255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        # mask2 = cv2.inRange(hsv2, lower_yellow, upper_yellow)

        #Bitwise-AND mask and original image
        res= cv2.bitwise_and(crop_img,crop_img, mask=mask)
        
        # Calculate centroid of the blob of binary image using ImageMoments for both images
        m = cv2.moments(mask, False)
        # m2 = cv2.moments(mask2, False)

        global line_confirm

        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
            line_finder= False
            line_confirm= True
        except ZeroDivisionError:
            cx, cy = height/2, width/2
            line_finder = True
        
        # Draw the centroid in the resultut images
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) 
        cv2.circle(mask,(int(cx), int(cy)), 1,(0,0,255),-1)

        cv2.circle(res,(int(cx), int(cy)), 1,(0,0,255),-1)
        # cv2.circle(mask2,(int(cx2), int(cy2)), 10,(0,0,255),-1)

        # Print the camera image, no changes
        cv2.imshow("Original", cv_image)
        # Print the primary mask image
        cv2.imshow("Primary Mask", mask)
        # Print the secondary mask image
        # cv2.imshow("Secondary Mask", mask2)
        cv2.imshow("res",res)
        cv2.waitKey(1)

        # Determine the error of the centroid with the middle of the image for 
        # both images
        """Controller here"""
        err = cx - width/2
        twist_object=Twist()
        twist_object.linear.x = 0.1
        twist_object.angular.z = -float(err)/985

        #print("camera_feed",twist_object.linear.x)
        #print("camera_feed2",twist_object.angular.z)    

        rospy.loginfo("ANGULAR VALUE SENT===>"+str(twist_object.angular.z))

        if line_finder:
            if line_confirm==False:

                def callback(msg):
                    global right_dist
                    global left_dist
                    global front_dist
                  
                    front_scan = []
                    front_left_scan = msg.ranges[0:15]
                    front_right_scan= msg.ranges[344:359]
                    front_scan.extend(front_left_scan)
                    front_scan.extend(front_right_scan)

                    front_dist = min(front_scan)
                    #print('front',front_dist)

                    right_scan=[]
                    right = msg.ranges[290:330]
                    right_scan.extend(right)
                    right_dist = sum(right_scan)/len(right_scan)
                    #print('right=',right_dist)

                    left_scan=[]

                    left = msg.ranges[30:70]
                    left_scan.extend(left)
                    left_dist = sum(left_scan)/len(left_scan)
                    #print('left=',left_dist)

                    if front_dist>10:
                        front_dist=10
                    # if left_dist>1:
                    # 	left_dist = 0.5

                sub = rospy.Subscriber("/scan", LaserScan, callback)

                threshold = 0.7
                #velocity = 0.5
                front_error = threshold - front_dist
                #print('front_error=',front_error)
                if front_error > 0:
                    if right_dist > left_dist:
                        twist_object.angular.z = -5*(front_error)
                        twist_object.linear.x = 0.3/(front_error+1)
                        #print('right_turn = ',twist_object.linear.x)

                    elif right_dist < left_dist:
                        twist_object.angular.z = 3*(front_error)
                        twist_object.linear.x = 0.3/(front_error+1)
                        #print('left_turn = ',twist_object.linear.x)
                    else:
                        twist_object.angular.z = 0
                        twist_object.linear.x = 0.4

                else:
                    twist_object.linear.x = 0.2
                    #print('just_liner',twist_object.linear.x)
                    twist_object.angular.z=0

            if line_confirm:
                twist_object.linear.x= 0
                twist_object.angular.z = 0

        # Publish the command
        # self.cmd_vel_pub.publish(self.twist_object)
        self.moveTurtlebot3_object.move_robot(twist_object)
     
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
