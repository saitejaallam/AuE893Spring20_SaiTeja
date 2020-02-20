HW03 : Team 7

In this assignment we have used the codes to move the turtle in a circle and square by continuously publishing the angular and linear velocities. We also created a world containing a wall and moved the turtlebot3 in that world.

Part 1:
The cirlcle.py file moves the turtlebot in a perfect circle in gazebo.

The square.py file moves the turtlebot with an angular velocity of 0.2 and linear velocity of 0.2 in gazebo.

The move.launch file launches the gazebo environment and brings in the turtlebot 3 burger in the environment itself. This launch file takes the code as an argument in the terminal which can be the square or the circle and execute it to move the turtlebot3 burger. The arguments to run the code are given in the move.launch file

Part 2:
An empty world is replace with a wall in it. This is just a simple environment.

The objective is to be able to execute an emergency braking maneuver on the turtlebot3 burger in the gazebo world when the turtlebot detects an obstacle (wall here) in front of it.

The turtlebot3_wall.launch file launches the gazebo world with wall. The world files are present in turtlebot3_simulations -->turtlebot3_gazebo --> world

It also continuously publishes the linear velocity and the distance of the turtlebot from the wall.

When the distance is less than 1, the turtlebot will stop moving forward.

The screecaptures are provided in the videos directory.


Commands:
The commands to run the codes in part 1 are 
a) roslaunch assignment3 move.launch code:=circle
b) roslaunch assignment3 move.launch code:=square

The command to run the code in part 2 is
roslaunch assignment3 turtlebot3_wall.launch

The work has been shared between all the 5 people in the team equally where individuals worked on different tasks and contributed to complete the tasks
1) Alec and saiteja worked on part 1.
2) Ajith worked on part 2 for emergency maneuvering.
2) Utkarsha and Ishan helped in resolving the errors obtained in task1 and task2.



