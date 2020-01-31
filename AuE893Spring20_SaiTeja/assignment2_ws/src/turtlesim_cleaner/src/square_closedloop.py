#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt

class TurtleBot():

    def __init__(self):
        #Creating our node,publisher and subscriber
        rospy.init_node('square_closedloop', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)

    #Callback function implementing the pose value received
    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidian_distance(self, goal_x, goal_y):
	"""Euclidean distance between current pose and the goal"""
        turtlesim_distance = sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
        return turtlesim_distance

    def move2goal(self):
	"""Moves the turtle towards the goal"""
	goal_coordinates = [[0,0], [0,0], [0,0], [0,0], [0,0]]
        goal_pose = Pose()

	for i in range (0,5):
	#Get the input from the user
	    x_pos = input("Set your x goal: ")
	    y_pos = input("Set your y goal: ")
	    goal_coordinates[x][0] = x_pos
	    goal_coordinates[x][1] = y_pos
	
        distance_tolerance = 0.5
        vel_msg = Twist()


	for j in range (0,5):
      	
	    while  sqrt(pow((goal_coordinates[i][0] - self.pose.x), 2) + pow((goal_coordinates[i][1] - self.pose.y), 2)) >= distance_tolerance:

            #Porportional Controller: choosing proportional gain 1.5
            #linear velocity in the x-axis:
                vel_msg.linear.x = 1.5 * sqrt(pow((coordinates[i][0] - self.pose.x), 2) + pow((coordinates[i][1] - self.pose.y), 2))
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0
	        vel_msg.angular.z = 0

 	        self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()

          
        #Stopping our robot after the movement is over
            vel_msg.linear.x = 0
            vel_msg.angular.z =0
            self.velocity_publisher.publish(vel_msg)

        rospy.spin()

if __name__ == '__main__':
    try:
        #Testing our function
        x = TurtleBot()
        x.move2goal()

    except rospy.ROSInterruptException: pass
