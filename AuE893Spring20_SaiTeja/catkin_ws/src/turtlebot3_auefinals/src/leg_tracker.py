#!/usr/bin/env python
import tf
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image, LaserScan
#from people_msgs.msg import PositionMeasurementArray
#from people_msgs.msg import PositionMeasurement
from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseArray
#from visualization_msgs.msg import Marker
#from visualization_msgs.msg import MarkerArray
from nav_msgs.msg import Odometry
from tf2_msgs.msg import TFMessage
from math import pow,atan2,sqrt
from tf.transformations import euler_from_quaternion, quaternion_from_euler


def callback_bot(msg):
	global x_bot,y_bot,z_bot
	global roll,pitch,yaw
	x_bot =msg.pose.pose.position.x
	y_bot =msg.pose.pose.position.y
	z_bot =msg.pose.pose.position.z

	orientation_q = msg.pose.pose.orientation
	quaternion = (orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)

	euler = tf.transformations.euler_from_quaternion(quaternion)
	roll =euler[0]
	pitch = euler[1]
	yaw = euler[2]

	return x_bot,y_bot,z_bot,yaw


def callback(data):

	pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)

	x_leg = data.poses[0].position.x
	y_leg  = data.poses[0].position.y
	z_leg = data.poses[0].position.z
	#print(x_det,y_det,z_det)

	twist_object = Twist()

	# lateral error
	x_error = x_leg-x_bot
	print(x_error)
	#longitudinal error
	y_error = y_leg-y_bot
	print('y:',y_error)

    #distance between man and bot
	dist = sqrt((x_error)**2 + (y_error)**2)
	print("dist",dist)

	rad = atan2(y_error,x_error)
	print("rad1",rad)

	theta = rad - yaw
	print("angle:", theta)
	#controller gains
	kp_ang = 0.8
	kp_lin = 0.2
	
	if dist>=0.2:
		twist_object.linear.x = dist*kp_lin
		twist_object.angular.z = (theta)*kp_ang
	
	pub.publish(twist_object)

	
def follow_leg():
#Let's Initialize ROS node
	rospy.init_node('detect_leg',anonymous=True)
	sub = rospy.Subscriber('/odom',Odometry,callback_bot)
	subscriber = rospy.Subscriber('/to_pose_array/leg_detector',PoseArray,callback)
	
	
	try: 
		rospy.spin()
	except KeyboardInterrupt:
		print "shutting down the controller"


if __name__ == '__main__':
	follow_leg()
