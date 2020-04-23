#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from darknet_ros_msgs.msg import BoundingBoxes
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

s=0

def callback(data):
	global label
	for box in data.bounding_boxes:
		label = format(box.Class)

	return label

def position(msg):
	move =Twist()
	pub =rospy.Publisher('/cmd_vel', Twist,queue_size=10)
	x0 = msg.pose.pose.position.x
	y0 = msg.pose.pose.position.y
	X1 = 1.2689 - 0.5
	X2 = 1.2689 + 0.5
	Y1 = -0.587152 -0.5
	Y2 = -0.587152 +0.5

	pub.publish(move)

	if ((X1<x0<X2) and (Y1<y0<Y2)):
		print("I am inside")
		if label == 'stop sign':
			global s
			s=s+1
			print("detected stop sign")
			t1 = float(rospy.Time.now().to_sec())
			t2 = t1
			if s==1:
			#while (Y1<y0<Y2):
				while ((t2-t1)<=3):
					move.linear.x = 0

					move.angular.z =0
					t2= float(rospy.Time.now().to_sec())
					print("stoppin",t2-t1)
					print("speed is",move.linear.x)

			else:
				move.linear.x = 0.2
				print("Bye Bye")
		else:
			move.linear.x=0.1

	else:
		move.linear.x=0.1

	pub.publish(move)

def main():
	rospy.init_node('stop',anonymous=True)
	rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes, callback)
	rospy.Subscriber('/odom',Odometry, position)

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "shutting down the controller"

if __name__ == '__main__':
	main()
