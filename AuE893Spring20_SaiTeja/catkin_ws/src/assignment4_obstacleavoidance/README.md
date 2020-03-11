Group 7
Alec Tokosch, Teja Allam, Utkarsha Chaudhari, Ajith Challa, and Ishan Sharma
AuE893 Spring 2020
Assignment 4 - Obstacle avoidance 

Explanation of files: 
wall_follower.py - the python script for the first part of the assignment. This file will allow the turtlebot to follow the path created by two walls. For controlling the motion we used the p-controller in the real world and also in the Gazebo environment. In Gazebo the variable Kp needs to be set to 0.6, for the real world the variable needs to be set to 2. 

Wander.py - the python script for the second part of the assignment. This file will allow the turtlebot to roam around without an direct goal other than avoiding obstacles within its path. For running the file, in Gazebo the variable Kp (proportional gain for P-controller) needs to be set to 0.4, for the real world the variable needs to be set to 0.8. 


The command to launch the codes are as follows
Part 1: roslaunch assignment4_obstacleavoidance turtlebot3_obstaceavoidance.launch
Part 2: roslaunch assignment4_obstacleavoidance turtlebot3_wall_follower.launch

Contributions:
Writing the script (wall_follower.py): Saiteja and Ajith started the code and got stuck with some errors then everyone sat in a group to discuss and debug the code. Finally, Alec finished debugging the code and commented it. 

Writing the script (wander.py): Started with the wall_follower.py and modified it as a group to include scanning multiple angles and the original controllers for the speed and rotation. Alec finished debugging, modified to average every 10 degrees of lidar data, found the minimum from the averaged ranges. Alec and Utkarsha added more logic to account for angled objects and coming up to a corner of the wall. Alec commented the code.

Tweaks to the scripts for gazebo and Real-time environment: While trying to run it on the real world we have to make some changes to the script by changing the Kp suitable for real world

Setting up & Testing in the Real-time Environment: All the team members were present while testing the code on the turtlebot. Ishan joined us on a skype call while testing the turtlebot. The cardboard boxes from the Armlab are used as the obstacles. 

Running code on the Turtlebot: Utkarsha was the first to figure out running code on the Turtlebot and showed others how to do it as well. 

Readme: Ishan, Alec and Teja wrote and edited the readme file.

