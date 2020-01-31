#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg	import Pose
import math
import time
from std_srvs.srv	import Empty



def circle_turtle(linear_speed, angular_speed, anticlockwise):
	


if _name_='_main_':
    try:
        rospy.init_node('turtlesim_motion_pose',anonymous=True)
	cmd_vel_topi = '/turtle1/cmd_vel'
	velocity_publisher = rospy.Publisher(cmd_vel_topic.Twist, queue_size=10)
	position_topic = "/turtle1/pose"
	pose_subscirber = rospy.Subscriber(position_topic, Pose, PoseCallback)
	time.sleep(2)
        
