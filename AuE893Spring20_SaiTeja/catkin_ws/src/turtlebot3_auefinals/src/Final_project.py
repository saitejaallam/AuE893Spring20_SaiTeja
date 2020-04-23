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

# Set global variables to be used within the code
line_confirm = False		# Lane confimation for detection
right_dist = 0				# Distance on the right side of the robot
left_dist = 0				# Distance on the left side of the robot
front_dist = 0				# Distance on the front of the robot
X1 = 0						# For virtual bounding box around stop sign
Y1 = 0						# For virtual bounding box around stop sign
X2 = 0						# For virtual bounding box around stop sign
Y2 = 0						# For virtual bounding box around stop sign
err = 0						# For error in the blob for line tracking, use to put the blob in the middle of the frame
s = 0						# For knowing when the stop sign is detected and the bot is within the area

class LineFollower(object):

    def __init__(self):
        self.bridge_object = CvBridge()
        self.stop_sub = rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes,self.stop_callback)
        self.position_sub = rospy.Subscriber('/odom',Odometry,self.position_callback)
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.person_sub = rospy.Subscriber("/to_pose_array/leg_detector",PoseArray,self.person_callback)

        self.moveTurtlebot3_object = MoveTurtlebot3()

        pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)

        twist_object = Twist()

    # Call back function for the stop sign, this returns the label of the object detected from hte bounding box
    def stop_callback(self,img):
        global label
        for box in img.bounding_boxes:
            label = format(box.Class)
    
        return label

    # Call back function for the position of the robot using the odometry. Using the bot orientation and position, 
    # we get the quaternions. The roll, pitch, and yaw can be obtained from quaternions. This will be used for 
    # leg tracking and to know the orientation of bot with respect tp human
    def position_callback(self,yolo):
    	# Declare the variables
        global x_bot,y_bot,z_bot,X1,X2,Y1,Y2
        global roll,pitch,yaw

        # Get the position of the robot
        x_bot = yolo.pose.pose.position.x
        y_bot = yolo.pose.pose.position.y
        z_bot = yolo.pose.pose.position.z

        # Get the orientaiton of the robot
        orientation_q = yolo.pose.pose.orientation

        # Loads the quaternions of the robot
        quaternion = (orientation_q.x,orientation_q.y,orientation_q.z,orientation_q.w)

        # Use the tranformations and convert to euler from quaternion to get the roll, pitch, and yaw. 
        euler = tf.transformations.euler_from_quaternion(quaternion)
        roll = euler[0]
        pitch = euler[1]
        yaw = euler[2]

        # Return the values that are needed
        return x_bot, y_bot, z_bot, yaw

    # Camera callback function for line following, also includes wall following and obstacle avoidance codes
    def camera_callback(self,data):

        # We select bgr8 because its the OpneCV encoding by default
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)    
            
        # We get image dimensions and crop the parts of the image we dont need
        height, width, channels = cv_image.shape

        # Values that can easily be changed to change the dimensions of the image for
        # line following
        descentre = 220
        rows_to_watch = 20

        # Crop the primary mask image to be very small
        #crop_img = cv_image[(height)/2 + descentre:(height)/2 + (descentre + rows_to_watch)][1:width]
        crop_img = cv_image[(height)/2:(height)/2 + (descentre + rows_to_watch)][1:width]
        
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
        
        # Calculate centroid of the blob of binary image using ImageMoments for both images
        m = cv2.moments(mask, False)
        
        global line_confirm
        
       	# Get the coordinates of the centroid (cx and cy)
        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
            line_finder = False
            line_confirm = True
            
        except ZeroDivisionError:
            cx, cy = height/2, width/2
            line_finder = True
        
        # Draw the centroid in the resultut images
        cv2.circle(mask,(int(cx), int(cy)), 1,(0,0,255),-1)

        # Print the camera image, no changes
        cv2.imshow("Original", cv_image)
        # Print the primary mask image
        cv2.imshow("Primary Mask", mask)
        cv2.waitKey(1)

        # Determine the error of the centroid with the middle of the image for 
        # both images
        """Controller here"""
        global err
        err = cx - width/2
        twist_object = Twist()

        # Publish the cmd_vel
        pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)

        # The area for the stop sign, used to know when the robot is within the virtual box
        # to know when to stop, this is essentially goefencing because without a stop line
        # the robot would not know where to actually stop. 
        X1 = 1.2689 - 1
        X2 = 1.2689 + 1
        Y1 = -0.587152 - 1
        Y2 = -0.587152 + 1

        # Set thresholds for the robot when wall following/obstacle avoidance
        Xmin_wall = -2
        Xmax_wall = 0.1
        Ymin_wall = -2
        Ymax_wall = 2

        # Set the twist to the twist_object since that is what we are calling the function below
        twist_object = Twist()
        
        # Declare the label variable to know what label is being detected by the darknet_ros
        global label

        #########################Obstacle Avoidance and Wall following############################### 
        
        # If no line has been found, then execute the wall following/obstalce avoidance code
        if line_finder:

            # If the robot is within the specified thresholds then execute the following:
            if ((Xmin_wall < x_bot < Xmax_wall) and (Ymin_wall < y_bot < Ymax_wall)):
            	# Verify that a line is not confirmed by the visual system, if so, then 
            	# avoid obstacles and follow the walls
                if ((line_confirm == False)):
                    
                    # Callback function for the laser scan data
                    def callback(msg):
                        # Declrare the global variables to be used
                        global right_dist
                        global left_dist
                        global front_dist
                      	
                      	# Get the front scans, 15 degrees each side
                        front_scan = []
                        front_left_scan = msg.ranges[0:15]
                        front_right_scan = msg.ranges[344:359]
                        front_scan.extend(front_left_scan)
                        front_scan.extend(front_right_scan)

                        # Get the minimum value from the front 30 degrees
                        front_dist = min(front_scan)

                        # Get the right scans, 40 degrees to the right
                        right_scan = []
                        right = msg.ranges[290:330]
                        right_scan.extend(right)

                        # Average the scans out on the right
                        right_dist = sum(right_scan)/len(right_scan)
                       
                        # Get the left scans, 40 degrees to the left
                        left_scan = []
                        left = msg.ranges[30:70]
                        left_scan.extend(left)

                        # Average the scans out on the left
                        left_dist = sum(left_scan)/len(left_scan)
                        #print('left=',left_dist)

                        # If the minimum front distance is greater than 10, aka likely infinite, 
                        # then set it to 10 since that is finite and it can be used as a control
                        # variable (gain)
                        if front_dist > 10:
                            front_dist = 10
                    
                    # Subscribe to the scan data
                    sub = rospy.Subscriber("/scan", LaserScan, callback)

                    # Set the threshold for obstacle avoidance
                    threshold = 0.7

                    # Calculate the error in the front based on the threshold and the 
                    # front distance
                    front_error = threshold - front_dist
                    #print('front_error=',front_error)

                    # If the front error is greater than 0, then the robot is too close to 
                    # an object in front and needs to turn. 
                    if front_error > 0:
                        
                        # Robot has more area/distance to the right, turn right
                        if right_dist > left_dist:
              
                            twist_object.angular.z = -5*(front_error)		# Will need to tune on each computer individually
                            twist_object.linear.x = 0.3/(front_error + 1)	# Will need to tune on each computer individually
                            pub.publish(twist_object)
                           

                        # Robot has more area/distance to the left, turn left
                        elif right_dist < left_dist:

                            twist_object.angular.z = 3.5*(front_error)		# Will need to tune on each computer individually
                            twist_object.linear.x = 0.25/(front_error + 1)	# Will need to tune on each computer individually
                            #print('doubt in obstacle ',twist_object.angular.z)
                            pub.publish(twist_object)
                        
						# Else, there is the same amount of area/distance on both sides, so 
						# just drive straight
                        else:
                            twist_object.angular.z = 0				# Will need to tune on each computer individually
                            twist_object.linear.x = 0.4				# Will need to tune on each computer individually
                           
                            pub.publish(twist_object)
                    
                    # Else, drive straight, but slower
                    else:
                        twist_object.linear.x = 0.2					# Will need to tune on each computer individually
                        twist_object.angular.z = 0					# Will need to tune on each computer individually
                        
                        pub.publish(twist_object)

 	##########################Stop Sign Recognition#########################

        else:
            print("entering line")
            # If stop sign is detected, then know need to stop soon
            if label == 'stop sign':

            	# Check if the robots position is within the virtual location determined 
            	# from the stop sign
                if ((X1 < x_bot < X2) and (Y1 < y_bot < Y2)):
                   
                    # Declare the global variable for the stop sign to know it has been 
                    # detected
                    global s

             
                    s = s + 1

                    # Get the current time, used to make sure the robot stops for 3 seconds
                    t1 = float(rospy.Time.now().to_sec())

                    # Set the current time to the previous time
                    t2 = t1

                    # If the stop sign has been detected, but only this first time, then
                    # need to stop the robot
                    if s == 1:

                    	# Stop the robot, set the linear and angular velocities to 0 for 
                    	# 3 seconds
                        while ((t2 - t1) <= 3):
                            print("stopping for 3 seconds")
                            twist_object.linear.x = 0
                            twist_object.angular.z = 0
                            t2 = float(rospy.Time.now().to_sec())
                            pub.publish(twist_object)

                    # Else, just continue to follow the line
                    else:
                        #print("first ")
                        twist_object.linear.x = 0.1				# Will need to tune on each computer individually
                        twist_object.angular.z = -float(err)/985	# Will need to tune on each computer individually
                        pub.publish(twist_object)

                # Else, just continue to follow the line
                else:
                    #print("second")
                    twist_object.linear.x = 0.1					# Will need to tune on each computer individually
                    twist_object.angular.z = -float(err)/985		# Will need to tune on each computer individually
                    pub.publish(twist_object)

            # Else, just continue to follow the line
            else:
                #print("executing code")
                twist_object.linear.x = 0.1						# Will need to tune on each computer individually
                twist_object.angular.z = -float(err)/985			# Will need to tune on each computer individually
                pub.publish(twist_object)

        return err   

       

    # Call back for the person
    def person_callback(self,human):
        print("following human")

        # Declare global variables for the humans position
        global X3,Y3,X4,Y4

        # Define global variable for line confirmation
        global line_confirm
        pub =rospy.Publisher('/cmd_vel',Twist,queue_size=10)

        # Get the location of the human
        x_leg = human.poses[0].position.x
        y_leg = human.poses[0].position.y
        z_leg = human.poses[0].position.z
        twist_object = Twist()

        # Calculate the error in the position between the robot and the humans legs
        x_error = x_leg - x_bot
        y_error = y_leg - y_bot

        # Calculate the distance between the the robot and the human using the distance 
        # formula and the errors between the robot and the human
        dist = sqrt((x_error)**2 + (y_error)**2)

        # Calculate the angle between the robot and the human using the errors between
        # the robot and the human
        rad = atan2(y_error,x_error)

        # Calculate the steering angle of the robot to follow the human
        theta = rad - yaw

        # Set the gains for the angular velocity and the linear velocity
        kp_ang = 0.8
        kp_lin = 0.3

        # Get the humans position within the 4th quadrant of the world
        X3 = human.poses[0].position.x - 1
        X4 = human.poses[0].position.x + 1
        Y3 = human.poses[0].position.y - 1
        Y4 = human.poses[0].position.y + 1 

        # If the distance between the robot and the human is less than 0.2, then do not move the 
        # robot towards the human anymore
        if dist < 0.2:
            twist_object.linear.x = 0
            twist_object.linear.z = 0
            print(dist)
            pub.publish(twist_object)

        # Else, the robot is not within 0.2 from the human, so move towards the human
        else:
           
            twist_object.linear.x = dist*kp_lin
            
            twist_object.angular.z = (theta)*kp_ang
          
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
