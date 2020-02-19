#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

# Assignment  - Turlebot

speedX = .2
speedAng = .2
distance = 2

def square():

    #Starts a new node
    rospy.init_node('turtlebot3_gazebo', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # Tell the user what is going to happen
    print("Let's make a 2x2 square")
    
    relative_angle = 0.5*PI
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # For loop to get all four sides and corners
    for x in range(4):
        #Setting the current time for distance calculus
        t0 = float(rospy.Time.now().to_sec())
        current_distance = 0
        # Lets go straight and complete the side of the square
        # Tell the user the turtlebot is going to go straight
        print("Lets go straight")
        
        # Loop to move the turtlebot the specified distance 
        while(current_distance < distance):
            # Set the linear veloicty to the speedX which is .2
            vel_msg.linear.x = abs(speedX)
            vel_msg.linear.z = 0
            #Publish the velocity
            velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
            t1=float(rospy.Time.now().to_sec())
            #Calculates distancePoseStamped
            current_distance= speedX*(t1-t0)
        #After the loop, stops the robot
        vel_msg.linear.x = 0

        # Now, lets turn to do another side of the square
        # Tell the user the turtlebot is going to turn 
        print("Let's rotate")
        
       
        # Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        # Loop to turn the turtlebot the specified angle
        while(current_angle < relative_angle):
            # Set the speed for the turtlebot to turn at which is .2 rad/s
            
            vel_msg.angular.z = abs(speedAng)
            velocity_publisher.publish(vel_msg)
            t2 = rospy.Time.now().to_sec()
            current_angle = speedAng*(t2-t0)


        #Forcing our robot to stop
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)



if __name__ == '__main__':
    try:
        # Testing our function
        square()

    except rospy.ROSInterruptException:
        pass
