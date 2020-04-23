Final Project Team 7 - AuE 8930

This package guides the turtlebot3 burger through:
1. Parallel walls
2. Obstacle course
3. Line detection and following
4. Stop sign detection and wait for 3 seconds
5. Person detection and following

The tasks were divided amongst the team members as follows:
1. Ajith - Coded for stop sign detection and helped in installing the darknet_ros packages
2. Teja - Coded for leg_tracking and installed the necessary packages for leg detection from the people detection packages. Integrated the codes for line following and obstacle avoidance.
3. Teja and Ajith - Integrated the complete codes and fine tuned the gains
4. Alec - Integration of wall following,obstacle avoidance
5. Alec and Utkarsha - Integration of wall following, obstacle avoidance and stop sign detection codes
6. Utkarsha - Launch files and readme
7. Ishan - Worked on Harr cascade, Mobilenet packages instead of tiny yolo .His work is related to stop sign detection and also helped in debugging 

To run this package you will need the following:
1. Turtlebot3 burger with a raspi camera http://gazebosim.org/tutorials?tut=ros_gzplugins#Camera
2. darknet package https://github.com/leggedrobotics/darknet_ros/tree/master/darknet_ros
3. opencv pakage https://github.com/ros-perception/vision_opencv
4. People detection package https://github.com/wg-perception/people

To run the package please execute the following command

'''
roslaunch turtlebot3_auefinals turtlebot3_autonomy_final.launch
'''

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
