# TurtlesimMotion
A simple repository which helps to play with the Turtlesim simulator

Once a standard ROS installation is made create the catkin workspace and include the python script inside the workspace and perform a catkin_make function to comple the code. Then move to the folder of the script and since it is a python script it needs to be made executable. chmod +x linear_angular_motion.py will make the code executable.

Once the code is made executable run the following set of commands in a terminal to get started with it:

roscore

ctrl+shift+t

rosrun turtlesim turtlesim_node

rosrun <pkg name where the script is placed> linear_angular_motion.py
  
This will show a interactive display where we get to choose linear motion, angular motion or another motion where we could enter the coordinates to be reached by the turtlseim and make it move there autonomously.

try this repository and have fun playing with the turtlseim !!!
