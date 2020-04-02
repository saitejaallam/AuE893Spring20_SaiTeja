Group 7
Alec Tokosch, Sai Teja Allam, Utkarsha Chaudhari, Ajith Challa, and Ishan Sharma
AuE893 Spring 2020
Assignment 5 - Tracking and Following

APPROACH:
PART 1: LINE FOLLOWING

1) Adding a camera to the turtlebot 3 burger to launch the camera module in gazebo. For that we changed the turtlebot3_burger.gazebo.xacro and turtlebot3_burger.urdf.xacro which are present in the urdf folders of the turtlebot3_description package.
2) To launch the custom world with yellow line we added the following line in bashrc file : export GAZEBO_MODEL_PATH=/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/assignment5_trackingandfollowing/models
3) We implemented the controller in the follow_line_step_hsv.py to move the tb3 burger in a gazebo simulated environment. Here we are using the Vision_opencv stack which contains the Cv bridge package with Cv_bridge ROS library.
4) We use two masks, a primary which is a small window and a secondary which is a much larger window in the gazebo environment. The python script contains two if conditions to define the motion of the bot.
5) Before testing it on the real bot we used a 8*6 printed checkerboard with each square of size 0.0254m and calibrated by taking 40 samples.

For calibration, we did turtlebot bringup and also bringup rpicamera, then we ran the following terminal commands for calibration

$ rosrun image_transport republish compressed in:=raspicam_node/image raw out: raspicam_node/image_raw

$ rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.0254 image:=/raspicam_node/image_raw camera:=/raspicam_node

6) Once the camera is calibrated we tested the same code on the real world bot by keeping the orange colour line and changing the color detection range in the python script but finally tested on the yellow line and also captured a video. We also captured a video in which the real bot followed a yellow object. During this implementation we used the image_transport package and also image_proc package in the image_pipeline stack which are also being pushed along with the assignment files.

PART 2: APRILTAG DETECTION(TRACKING)

1) To start with this assignment we cloned the april tag libraries and apriltag_ros package from https://github.com/AprilRobotics/apriltag_ros and https://github.com/AprilRobotics/apriltag
2) We built the package by catkin_make_isolated to make the packages as suggested from the readme file of the above mentioned github repositories.
3) We chose apriltag from the family of 36h11 with an id 3. The tag details are updated in the apriltag_ros/apriltag_ros/config/tags.yaml along with the size of the tag
4) This apriltag_ros comes up with a conitnuous_detection.launch which calls up the apriltag_ros_continuous_node.cpp node in the src folder.
5) To obtain the raw image we used image_transport node and then used image_proc node from the image_pipeline stack. After these terminals we launched the continuous_detection.launch which gives the tag_detections topic.
6) When the camera started detecting, we wrote a code to move the bot by tracking the tag. We captured a video which are provided here in the following location assignment5_trackingandfollowing/videos.
7) The launch file for this part includes calling the image_transport, image_proc and the tag_follower.py nodes at one place.

The command to launch the codes are as follows:

PART 1:LINE_FOLLOWING
Gazebo -  roslaunch assignment5_trackingandfollowing turtlebot3_follow_line.launch
Real world - roslaunch assignment5_trackingandfollowing turtlebot3_follow_line_realworld.launch

PART 2: APRILTAG_DETECTION
roslaunch apriltag_ros continuous_detection.launch

CONTRIBUTIONS:
Alec 
He created the code to implement the line following on the gazebo simulated environment.
Alec modified the files necessary to implement the camera on the burger in Gazebo.
Alec and Utkarsha took charge to install the camera on the real Turtlebot.

Utkarsha
Installed the camera on the real turtlebot along with Alec.
Implemented the line following on the real turtlebot by using the orange lines instead of yellow lines.
Calibrated the camera required to implement on the turtlebot.

Ishan
worked on Kobuki base implementing the two tasks because he doesnot have access to the turtlebot3 burger.

Ajith
Implemented the line following, april detection codes on turtlebot and helped teja in capturing the videos and resolving the issues in part 2.

Sai Teja
modified the launch file for line following code by including the image_transport node and calling the follow_line_step_hsv_realworld.py node.
Generated the code for tag_detection and created the launch file for part 2.

The videos for both the parts are provided in assignment5_trackingandfollowing/videos.


NOTE:

The github repository contains the apriltag_ros package which has all the relevant packages to run part2. As it was built with catkin_make_isolated it cannot be kept in the assignments catkin_ws which was built with catkin_make. So for easy readability and grading I copied the launch file and scripts in the respective launch and src folders of assignment5_trackingandfollowing package. Please clone the apriltag_ws to test on the bot.



