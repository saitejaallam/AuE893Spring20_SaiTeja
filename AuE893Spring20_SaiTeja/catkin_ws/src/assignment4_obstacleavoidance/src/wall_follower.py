#!/usr/bin/env python
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
#from rospy import Time
import rospy
import numpy as np
import math

# Assignment 4, Obstacle Avoidance, team 7.

# Set global variables to be used for saving the last finite value for left and right
# scans of the lidar.
previous_left = 0
previous_right = 0

def callback(msg):
    # Define global variables
    global previous_left
    global previous_right

    # Propertional gain for turning the turtlebot
    Kp = 0.6      # .6 in gazebo, real world 2
        
    # Get the scan data for that is to the left, 60 to 70 degrees (starting from center at 0)
    left_scan  = msg.ranges[60:70]

    # Get the scan data for that is to the right, 289 to 299 degrees (starting from center at 0)
    right_scan = msg.ranges[289:299]
    #straight_wall = sum(center_scan)/5
    
    # Average the scans on the left to get a more accurate representation of the distance
    left_wall = sum(left_scan)/10
    
    # Average the scans on the right to get a more accurate representation of the distance
    right_wall = sum(right_scan)/10

    # If the distance is too far to the wall to get an accurate reading, or cannot get a reading
    # then set it to the previously known good value that is finite
    if left_wall == float("inf"):
        left_wall = previous_left
   
    # If the distance is too far to the wall to get an accurate reading, or cannot get a reading
    # then set it to the previously known good value that is finite
    elif right_wall ==float("inf"):
        right_wall = previous_right


    # Find the difference between the turtlebot and the left and the right walls to try and
    # center the trutlebot between the two walls. If the result is positive, then the turtlebot
    # is too close to the right wall and needs to move towards the left wall, if the results is
    # negative, then the turtlebot is too close to the left wall and needs to move towards the
    # right wall.
    center = left_wall-right_wall

    # Set the forward velocity in the x direction
    move.linear.x = 0.3

    # Set the angular velocity in z, controller handles turning left or right.
    # If the value is positive then it will turn left, if the value is negative then
    # it will turn right.
    steer_control = Kp*center
    move.angular.z = steer_control
    
    pub.publish(move)
    
    # Save the previous finite values for the distance to the left and the right wall to be
    # used if a distance is determined to be infinite.
    previous_left = left_wall
    previous_right = right_wall


move = Twist() # Creates a Twist message type object
rospy.init_node('wall_follower_node',anonymous= True) # Initializes a node
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

sub = rospy.Subscriber("/scan", LaserScan, callback)
                              
rospy.spin()
