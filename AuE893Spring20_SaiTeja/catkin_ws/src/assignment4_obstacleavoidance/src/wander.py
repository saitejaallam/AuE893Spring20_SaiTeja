#!/usr/bin/env python
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
#from rospy import Time
import rospy
import numpy as np
import math

# Assignment 4, Obstacle Avoidance, team 7.


def callback(msg):

    # Propertional gain for turning the turtlebot, 0.8 for physical world and 0.4 for Gazebo
    Kp = 0.8    # 0.4 or 0.8

    # Proportional gain for moving the bot forward. If this is changed to be larger, the
    # threshold needs to be larger or it will be very close to hitting the wall, and may
    # hit the wall when attempting to turn around.
    Kp_forward = 0.3    # NOTE: if this is changed, need to change threshold

    # Threshold variable for distance from objects, do not change to be too low
    threshold = 0.4

    # Variable to move forward
    throttle = 0

    # Variable to turn
    steer_control = 0

    # Get the scan data for that is to the left, 30 degrees (starting from center at 0)
    forward_left_scan  = msg.ranges[0:30]

    # Get the scan data for that is to the right, 329 to 359 (-30) degrees to the right,
    # (starting from center at 0)
    forward_right_scan  = msg.ranges[329:359]

    # Split the 30 degree segement on the left into 3 different parts that are 10 degree
    # each. Average the readings in each 10 degree window. This will make it easier to
    # detect objects in the range. Averaging across all of the values makes it more
    # difficult to detect objects in the range from 0 to 30 degrees.
    forward_left1 = sum(forward_left_scan[0:10])/10
    forward_left2 = sum(forward_left_scan[10:20])/10
    forward_left3 = sum(forward_left_scan[20:30])/10

    # Do the same for the right
    forward_right1 = sum(forward_right_scan[0:10])/10
    forward_right2 = sum(forward_right_scan[10:20])/10
    forward_right3 = sum(forward_right_scan[20:30])/10

    # From the averaged values from the left, find the minimum to know if there is an object
    # within the path of the turtlebot on the left in one of the 10 degree windows.
    forward_left = min(forward_left1, forward_left2, forward_left3)

    # Do the same for the right to know if there is an object in the path on the right
    forward_right = min(forward_right1, forward_right2, forward_right3)

    # For Gazebo, if the minimum value is infinite, then set it to a value of 4 for both
    # left and right values. For real world, if the value is zero, then it is infinite and
    # needs to be set to a value.
    if forward_left == float("inf") or forward_left == 0:
        forward_left = 4

    if forward_right == float("inf") or forward_right == 0:
        forward_right = 4

    # Get the minimum forward distance between the left and the right front readings, this
    # is used for determining the value to move forward by
    front = min (forward_right, forward_left)


    # Getting the scan data from left and right
    # Get the scan data for that is to the left, 20 to 90 degrees (starting from center at 0)
    left_scan  = msg.ranges[20:90]

    # Get the scan data for that is to the right, 269 to 339 degrees (starting from center at 0)
    right_scan = msg.ranges[269:339]

    # Note: The range for the left and right overlap with the forward ranges by 10 degrees. This
    # was done intentionally to help detect objects that the turtlebot could potentially hit, this
    # allows the turtlebot to avoid these objects
    
    # Using 10 degree increments again, average the data every 10 degrees.
    left_wall1 = sum(left_scan[0:10])/10
    left_wall2 = sum(left_scan[10:20])/10
    left_wall3 = sum(left_scan[20:30])/10
    left_wall4 = sum(left_scan[30:40])/10
    left_wall5 = sum(left_scan[40:50])/10
    left_wall6 = sum(left_scan[50:60])/10
    left_wall7 = sum(left_scan[60:70])/10
    
    # Do the same for the right side
    right_wall1 = sum(right_scan[0:10])/10
    right_wall2 = sum(right_scan[10:20])/10
    right_wall3 = sum(right_scan[20:30])/10
    right_wall4 = sum(right_scan[30:40])/10
    right_wall5 = sum(right_scan[40:50])/10
    right_wall6 = sum(right_scan[50:60])/10
    right_wall7 = sum(right_scan[60:70])/10

    # For Gazebo, if the value is infinite, then set it to a value of 4.xx, for both left and
    # right values. For real world, if the value is zero, then it is infinite and needs to be
    # set to a value.
    if left_wall1 == float("inf") or left_wall1 == 0:
        left_wall1 = 4.1
    
    if left_wall2 == float("inf") or left_wall2 == 0:
        left_wall2 = 4.15

    if left_wall3 == float("inf") or left_wall3 == 0:
        left_wall3 = 4.2

    if left_wall4 == float("inf") or left_wall4 == 0:
        left_wall4 = 4.25
    
    if left_wall5 == float("inf") or left_wall5 == 0:
        left_wall5 = 4.3

    if left_wall6 == float("inf") or left_wall6 == 0:
        left_wall6 = 4.35

    if left_wall7 == float("inf") or left_wall7 == 0:
        left_wall7 = 4.4

    if right_wall1 == float("inf") or right_wall1 == 0:
        right_wall1 = 4.1
    
    if right_wall2 == float("inf") or right_wall2 == 0:
        right_wall2 = 4.15

    if right_wall3 == float("inf") or right_wall3 == 0:
        right_wall3 = 4.2

    if right_wall4 == float("inf") or right_wall4 == 0:
        right_wall4 = 4.25
    
    if right_wall5 == float("inf") or right_wall5 == 0:
        right_wall5 = 4.3

    if right_wall6 == float("inf") or right_wall6 == 0:
        right_wall6 = 4.35

    if right_wall7 == float("inf") or right_wall7 == 0:
        right_wall7 = 4.4


    # Find the minimum value between all of the segments on the left, including the forward left values.
    # This will provide a detection in one of the 10 degree windows. The forward left minimum value is included here
    # to help determine if there is an object in front on the left - this helps with turning the turtlebot when
    # there is an object straight ahead and at an angle.
    left_min = min(left_wall1, left_wall2, left_wall3, left_wall4, left_wall5, left_wall6, left_wall7, forward_left)
    
    # Find the maxmim value between all of the segments on the left, this doesn't include the forward left values
    # because we only care if there isn't an object in front when looking for the maximum value.
    left_max = max(left_wall1, left_wall2, left_wall3, left_wall4, left_wall5, left_wall6, left_wall7)

    # Do the same for the right maximum and minimum
    right_min = min(right_wall1, right_wall2, right_wall3, right_wall4, right_wall5, right_wall6, right_wall7, forward_right)
    right_max = max(right_wall1, right_wall2, right_wall3, right_wall4, right_wall5, right_wall6, right_wall7)

    
    # Look to see if anything is in front or on the sides, if nothing, then
    # move forward
    if front > threshold and left_min > threshold and right_min > threshold:
        throttle = front * Kp_forward
        steer_control = 0
        #print("forward", front)

    # Check if anything is in front, if so, then check the sides before turning
    elif front <= threshold:

        # Turn whichever: Check if anything is to the right and left, turn to which
        # ever has more room when the distances are greater than the threshold.
        if left_min > threshold and right_min > threshold:
            throttle = 0
            steer_control = Kp * (left_min - right_min)
            #print("turn whichever if greater", left_min, right_min)

        # Turn right: If the turtlebot is too close to the left wall and the distance to the
        # right wall is greater than the threshold, then turn to the right.
        elif left_min <= threshold and right_min > threshold:
            throttle = front * Kp_forward
            steer_control = -Kp * right_min
            #print("turn right", left_min)

        # Turn left: If the turtlebot is too close to the right wall and the distance to the
        # left wall is greater than the threshold, then turn to the left.
        elif right_min <= threshold and left_min > threshold:
            throttle = front * Kp_forward
            steer_control = Kp * left_min
            #print("turn left", right_min)

        # Turn whichever is greater: Both are less than the threshold, then find the maximum
        # value between the left and the right side scans to turn to whichever has more room.
        # If the difference between the left and right maximums is less than 0.07, then do not
        # use the controller to turn because it will be very slow, then just turn with an angular
        # velocity of 0.5.
        elif left_min <= threshold and right_min <= threshold:
            throttle = 0

            if (left_max - right_max) > 0.07:
                steer_control = Kp * (left_max - right_max)
            else:
                steer_control = .5
            
            #print("both less than threshold", left_max, right_max, (left_max - right_max))

        # If not close enough with the sides yet, but picking up something in the path on the
        # front left and the distance is less than the threshold, then need to turn to the right
        # to avoid it
        elif forward_left <= threshold:
            throttle = front * Kp_forward
            steer_control = -Kp * forward_right
            #print("front left, turn right", forward_left)

        # If not close enough with the sides yet, but picking up something in the path on the
        # front right and the distance is less than the threshold, then need to turn to the left
        # to avoid it
        elif forward_right <= threshold:
            throttle = front * Kp_forward
            steer_control = Kp * forward_left
            #print("front right, turn left", forward_right)
        
        # Fail safe, stop moving forward and turn to the left
        else:
            throttle = 0
            steer_control = 1
            #print("Failsafe 2")
    
    # If the forward distance is not less than the threshold, but the scans to the left are
    # less than the threshold, then the turtlbot needs to turn to the right
    elif left_min <= threshold:
        throttle = front * Kp_forward
        steer_control = -Kp * right_min
        #print("turn right, but no object in front", left_min)


    # If the forward distance is not less than the threshold, but the scans to the right are
    # less than the threshold, then the turtlbot needs to turn to the left
    elif right_min <= threshold:
        throttle = front * Kp_forward
        steer_control = Kp * left_min
        #print("turn left, but no object in front", right_min)

    # Fail safe, stop moving forward and turn, should never get to this
    else:
        throttle = 0
        steer_control = 1
        #print("Failsafe 1")

    # Set the variables for the linear and angular movements.
    move.linear.x = throttle
    move.angular.z = steer_control

    pub.publish(move)


move = Twist() # Creates a Twist message type object
rospy.init_node('wall_follower_node',anonymous= True) # Initializes a node
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

sub = rospy.Subscriber("/scan", LaserScan, callback)
                              
rospy.spin()

