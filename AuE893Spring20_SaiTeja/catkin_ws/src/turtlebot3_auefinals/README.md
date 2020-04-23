Group 7
Alec Tokosch, Sai Teja Allam, Utkarsha Chaudhari, Ajith Challa, and Ishan Sharma
AuE893 Spring 2020
Assignment 5 - Tracking and Following

Approach:
#####################Wall Following/Obstacle Avoidance##########
1. We used the code we had generated in the previous assignments and modified a bit to integrate the wall following and obstacle avoidance in one code. 
2. We used the gmapping Slam which is available in the Maps folder of the turtlebot3_auefinals package.
3. We changed an obstacle height in the course as it is not visible to the turtlebot's lidar scan

#####################Line Following and stop sign detection####################
1. We integrated the line follwoing code with the wall following and obstacle avoidance. We reduced the blob size and the crop image ratios to follow the line perfectly at the center. 
2. We created a code for stop sign, tested it separately and integrated it to the main code.

#######################Human Tracking#######################
1. The challenge we found here is finding the correct dependencies to the packages that we wanted to use for leg tracking.
2. We deleted all the unnecessary packages and left with people, strands_perceptio_people, tc_people_tracker.
3. We had to clone one other package wu_ros_tools which we figured when we get a dependency error for easy markers.

These package guides the turtlebot3 burger through:
1. Parallel walls
2. Obstacle course
3. Line detection and following
4. Stop sign detection and wait for 3 seconds
5. Person detection and following


########################################### Contributions#########################################################
The tasks were divided amongst the team members as follows:
1. Ajith - Coded for stop sign detection and helped in installing the darknet_ros packages
2. Teja - Coded for leg_tracking and installed the necessary packages for leg detection from the people detection packages. Integrated the codes for line following and obstacle avoidance.
3. Teja and Ajith - Integrated the complete codes and fine tuned the gains
4. Alec - Integration of wall following,obstacle avoidance. He figured out the problem with the obstacles height which has not been recognised by the lidar scan data.
5. Alec and Utkarsha - Integration of wall following, obstacle avoidance and stop sign detection codes
6. Utkarsha - Launch files and readme
7. Ishan - Worked on Harr cascade, Mobilenet packages instead of tiny yolo .His work is related to stop sign detection and also helped in debugging 

To run this code you will need the following:
1. Turtlebot3 burger with a raspi camera http://gazebosim.org/tutorials?tut=ros_gzplugins#Camera
2. darknet package https://github.com/leggedrobotics/darknet_ros/tree/master/darknet_ros
3. opencv pakage https://github.com/ros-perception/vision_opencv
4. People detection package https://github.com/wg-perception/people

To run the package please execute the following command

'''
roslaunch turtlebot3_auefinals turtlebot3_autonomy_final.launch
'''

#########################################Timed launch file################################################
As we are facing problem with our CPU power when we launch tiny yolo. We cloned a package to launch the launch files after a particular time. TO run the launch file you have to install the following package.
""" sudo apt install ros-<ros-distro>-timed-roslaunch """

The launch file will launch the following nodes:
1. Gazebo world with the turtlebot3 burger
2. Rviz
3. Gmapping
4. Python code for
	a. Wall following
	b. Obstacle avoidance
	c. Line following
	d. Stop sign detection
	e. Person tracking
   in this sequence
5. open_cv for line following
6. darknet_ros package for stop sign detection
7. leg_detection package for person tracking


Copy all the 7 packages in the zip folder and catkin_make 
