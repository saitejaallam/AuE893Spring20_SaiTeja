#!/usr/bin/env python
import rospy
#from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from rospy import Time


def callback(msg):
	
    move.linear.x = 0.3
	
    if msg.ranges[0]<=1:
        move.linear.x = 0
    pub.publish(move)


rospy.init_node('scan_values',anonymous =True)

scanval = rospy.Subscriber('scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
move=Twist()

rospy.spin()

rate = rospy.Rate(5)

while not rospy.is_shutdown():
    pub.publish(move)
    rate.sleep

