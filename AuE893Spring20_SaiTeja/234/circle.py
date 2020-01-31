#!/usr/bin/env python
import rospy
from geometry_msgs.msg      import Twist
from turtlesim.msg          import Pose
from std_srvs.srv           import Empty
PI = 3.14

def circle_turtle(linear_velocity, angular_velocity, anticlockwise):
    publisher = rospy.publisher('/turtle1/cmd_vel',Twist, queue_size = 10)
    rospy.init_node('turtlesim_Pose', anonymous=True)
    velocity_msg = Twist()
    rate = rospy.Rate(10)                   # 10hz

#print("Let's rotate the robot")
#speed = input("Input your speed (degrees/sec):")
#angle = input("Type your distance (degrees):")
#clockwise = input("Clockwise?: ") #True or false

#angular_speed  = speed*2*PI/360
#relative_angle = angle*2*PI/360

    velocity.linear.x = 0
    velocity.linear.y = 0
    velocity.linear.z = 0

    velocity.angular.x =0
    velocity.angular.y =0
    velocity.angular.z = angular_velocity

    while not rospy.is_shutdown():
        publisher.publish(velocity_msg)
        rate.sleep(10)
    #rospy.loginfo(linear_velocity, angular_velocity)

if __name__ == '__main__':
    try:
        circle_turtle(linear_velocity, angular_velocity)
    except rospy.ROSInterruptException:
        pass


