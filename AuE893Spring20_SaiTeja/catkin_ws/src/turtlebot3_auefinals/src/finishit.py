#!/usr/bin/env python
import tf
import cv2
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point,PoseArray
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, LaserScan
from move_robot import MoveTurtlebot3
from math import sqrt,pow,atan2
from darknet_ros_msgs.msg import BoundingBoxes
from std_msgs.msg import String, Header
from nav_msgs.msg import Odometry
from tf2_msgs.msg import TFMessage
from tf.transformations import euler_from_quaternion, quaternion_from_euler

line_confirm = False
right_dist = 0
left_dist = 0
front_dist= 0
X1=0
Y1=0
X2=0
Y2=0
err=0
s=0
#leg_tracker=False
#wall_follow =False

class LineFollower(object):

    def __init__(self):

        self.bridge_object = CvBridge()
        self.stop_sub = rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes,self.stop_callback)
        self.position_sub = rospy.Subscriber('/odom',Odometry,self.position_callback)
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.person_sub = rospy.Subscriber("/to_pose_array/leg_detector",PoseArray,self.person_callback)

        self.moveTurtlebot3_object = MoveTurtlebot3()

        pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)

        twist_object=Twist()

    def stop_callback(self,img):
        global label
        for box in img.bounding_boxes:
            label = format(box.Class)
    
        return label

    def position_callback(self,yolo):
        global x_bot,y_bot,z_bot,X1,X2,Y1,Y2
        global roll,pitch,yaw
        x_bot = yolo.pose.pose.position.x
        y_bot = yolo.pose.pose.position.y
        z_bot = yolo.pose.pose.position.z

        orientation_q = yolo.pose.pose.orientation
        quaternion = (orientation_q.x,orientation_q.y,orientation_q.z,orientation_q.w)

        euler = tf.transformations.euler_from_quaternion(quaternion)
        roll = euler[0]
        pitch = euler[1]
        yaw = euler[2]

        return x_bot, y_bot, z_bot, yaw

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
        crop_img = cv_image[(height)/2+descentre:(height)/2+(descentre+rows_to_watch)][1:width]
	    
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
       
        #Bitwise-AND mask and original image
        # res= cv2.bitwise_and(crop_img,crop_img, mask=mask)
        
        # Calculate centroid of the blob of binary image using ImageMoments for both images
        m = cv2.moments(mask, False)
        
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

        # cv2.circle(res,(int(cx), int(cy)), 1,(0,0,255),-1)
        # cv2.circle(mask2,(int(cx2), int(cy2)), 10,(0,0,255),-1)

        # Print the camera image, no changes
        cv2.imshow("Original", cv_image)
        # Print the primary mask image
        cv2.imshow("Primary Mask", mask)
        # cv2.imshow("res",res)
        cv2.waitKey(1)

        # Determine the error of the centroid with the middle of the image for 
        # both images
        """Controller here"""
        global err
        err = cx - width/2
        twist_object=Twist()

        pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)


        X1 = 1.2689 - 1
        X2 = 1.2689 + 1
        Y1 = -0.587152 - 1
        Y2 = -0.587152 + 1

        Xmin_wall = -2
        Xmax_wall = 0.1
        Ymin_wall = -2
        Ymax_wall =2

        twist_object=Twist()
        
        global label

        #rospy.loginfo("ANGULAR VALUE SENT===>"+str(twist_object.angular.z))

        ######################### Obstacle Avoidance and Wall following ###############################  
        if line_finder:

            if ((Xmin_wall<x_bot<Xmax_wall) and (Ymin_wall<y_bot<Ymax_wall)):

                if ((line_confirm==False)):
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

                        right_scan=[]
                        right = msg.ranges[290:330]
                        right_scan.extend(right)
                        right_dist = sum(right_scan)/len(right_scan)
                       
                        left_scan=[]

                        left = msg.ranges[30:70]
                        left_scan.extend(left)
                        left_dist = sum(left_scan)/len(left_scan)
                        
                        if front_dist>10:
                            front_dist=10
                       
                    sub = rospy.Subscriber("/scan", LaserScan, callback)

                    threshold = 0.7
                   
                    front_error = threshold - front_dist
             

                    if front_error > 0:
                        if right_dist > left_dist:
                            
                            twist_object.angular.z = -5*(front_error)
                            twist_object.linear.x = 0.3/(front_error+1)
                            pub.publish(twist_object)

                        elif right_dist < left_dist:

                            twist_object.angular.z = 3.5*(front_error)
                            twist_object.linear.x = 0.25/(front_error+1)
                           
                            pub.publish(twist_object)
                        else:
                            twist_object.angular.z = 0
                            twist_object.linear.x = 0.4
                      
                            pub.publish(twist_object)
                    else:
                        twist_object.linear.x = 0.2
                      
                        twist_object.angular.z=0
                        pub.publish(twist_object)

    ########################### Stop Sign Recognition ###############################
        else:
            print("entering line")
            if label == 'stop sign':

                if ((X1<x_bot<X2) and (Y1<y_bot<Y2)):
                
                    global s
                    s=s+1
                    t1= float(rospy.Time.now().to_sec())
                    t2 = t1

                    if s ==1:
                        while ((t2-t1)<=3):
                            print("stopping for 3 secs")
                            twist_object.linear.x = 0
                            twist_object.angular.z = 0
                            t2 = float(rospy.Time.now().to_sec())
                            pub.publish(twist_object)

                    else:
                        
                        twist_object.linear.x = 0.1
                        twist_object.angular.z = -float(err)/985
                        pub.publish(twist_object)

                else:
                    print("second")
                    twist_object.linear.x = 0.1
                    twist_object.angular.z = -float(err)/985
                    pub.publish(twist_object)

            else:
                print("executing code")
                twist_object.linear.x = 0.1
                twist_object.angular.z = -float(err)/985
                pub.publish(twist_object)
        
        return err   

    ########################## Leg Tracking #########################
    

    def person_callback(self,human):
        print("I am following human")
        global X3,Y3,X4,Y4

        global leg_tracker
        global line_confirm
        global wall_follow
        pub =rospy.Publisher('/cmd_vel',Twist,queue_size=10)

        x_leg = human.poses[0].position.x
        y_leg = human.poses[0].position.y
        z_leg = human.poses[0].position.z
        twist_object = Twist()
        

        x_error = x_leg - x_bot
        y_error = y_leg - y_bot

        dist = sqrt((x_error)**2 + (y_error)**2)
        rad = atan2(y_error,x_error)
        theta = rad -yaw
        kp_ang = 0.8
        kp_lin = 0.3

        X3 = human.poses[0].position.x - 1
        X4 = human.poses[0].position.x +1
        Y3 = human.poses[0].position.y - 1
        Y4 = human.poses[0].position.y + 1 

        if dist<0.2:
            twist_object.linear.x =0
            twist_object.linear.z = 0
            print(dist)
            pub.publish(twist_object)

        else:
            print("follow")
            twist_object.linear.x = dist*kp_lin
            print("human velcoity:", twist_object.linear.x)
            twist_object.angular.z = (theta)*kp_ang
            print("greater dist",dist)
            pub.publish(twist_object)
     
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
