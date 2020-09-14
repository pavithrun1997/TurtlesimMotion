#!/usr/bin/env python
""" 
This Code has three different functions
1.Linear Motion Function
2.Rotational Motion Function
3.Go_to_goal Function

The Linear Motion function takes in linear velocity,distance to be covered and the direction of motion
as the three parameters and makes the turtle to reach the position

The Angular Motion Function takes in angular velocity in degrees,angle of rotation in degrees and the 
direction of rotation as the three parameters. As ROS works with radians, we need to convert the 
angular velocity to radians before we proceed.This function makes the turtle to rotate and change the 
orientation as desired

The Go_to_goal function makes the turtle to move from the location where it is spawned to the desired co-
ordinates. The function takes in the x and y co-ordinates of the desired goal location and makes the turtle 
reach the same.
"""


import rospy
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

def linear_move(vel,dist,direct):           ## Function to publish velocity for linear travel
    rospy.loginfo("Info Recieved !!!")
    
    if (direct > 0):
        velocity.linear.x = abs(vel)

    else:
        velocity.linear.x = -abs(vel)
    
    distance_initial = 0.0
    loop_rate = rospy.Rate(10)
    t0 = rospy.Time.now().to_sec()

    while True:
            rospy.loginfo("Moving !!!")
            linear_velocity.publish(velocity)
            loop_rate.sleep()
            t1 = rospy.Time.now().to_sec()
            distance_initial = vel * (t1 - t0)
            print(distance_initial)
            if not (distance_initial < dist):
                rospy.loginfo("Reached")
                break
    
    velocity.linear.x = 0
    linear_velocity.publish(velocity)

def rotation_move(angular_speed_degree,desired_angle,direction_of_rotation):         ## Function to publish velocity for angular travel
    rospy.loginfo("Info Recieved !!")
    angular_speed=math.radians(abs(angular_speed_degree))

    if direction_of_rotation > 0:
        velocity.angular.z = abs(angular_speed)
    else:
        velocity.angular.z = -abs(angular_speed)
    
    angle_initial = 0.0
    loop_rate = rospy.Rate(10)
    t0 = rospy.Time.now().to_sec()
    while True:
        rospy.loginfo("Rotating !!")
        linear_velocity.publish(velocity)
        loop_rate.sleep()
        t1 = rospy.Time.now().to_sec()
        angle_initial = (t1-t0) * angular_speed_degree
        print(angle_initial)
        if not angle_initial < desired_angle:
            rospy.loginfo("Finish Rotating")
            break
    
    velocity.angular.z = 0.0
    linear_velocity.publish(velocity)


def pose_call_back(message):
    global x_turtle
    global y_turtle
    global yaw
    x_turtle = message.x
    y_turtle = message.y
    yaw = message.theta  
def orientation(x,y):
    global desired_angle_goal
    desired_angle_goal = math.atan2(y-y_turtle, x-x_turtle)
    while abs(desired_angle_goal-yaw) >= 0.1:
        velocity.linear.x = 0.0
        angular_speed = 0.1    
        velocity.angular.z = angular_speed
        linear_velocity.publish(velocity)
        rospy.loginfo( 'x= '+str(x_turtle)+'y= ' +str(y_turtle))
        rospy.loginfo(desired_angle_goal-yaw)
        rospy.loginfo("Still Rotating")
        rospy.sleep(1)
    velocity.angular.z = 0
    linear_velocity.publish(velocity)
    rospy.sleep(1)

def go_to_goal(x,y):                                        ## Function to make the turtle reach the goal
    rospy.Subscriber('/turtle1/pose',Pose,pose_call_back)  
    rospy.sleep(2)
    rospy.Rate(10)
    orientation(x,y)
    distance_to_goal = abs(math.sqrt(((x-x_turtle) ** 2) + ((y-y_turtle) ** 2)))
    try:
        while distance_to_goal > 0.1:
            linear_speed = 0.1
            velocity.linear.x = linear_speed
            linear_velocity.publish(velocity)
            rospy.loginfo( 'x= '+str(x_turtle)+'y= '+str(y_turtle))
            distance_to_goal = abs(math.sqrt(((x-x_turtle) ** 2) + ((y-y_turtle) ** 2)))
            rospy.loginfo(distance_to_goal)
            rospy.loginfo("Still moving")
            rospy.sleep(1)
            if desired_angle_goal >= 0.1:
                orientation(x,y)
                rospy.loginfo("Calling again for orientation")
            if distance_to_goal <= 0.1:
                rospy.loginfo("Reached")
                break
            
        velocity.linear.x = 0.0
        velocity.angular.z = 0.0
        linear_velocity.publish(velocity)
    
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")




if __name__ == '__main__':
    try:
        x_turtle = 0
        y_turtle = 0
        yaw = 0
        rospy.init_node('linear_angular_motion',anonymous=True)           ## Node Initialization
        linear_velocity = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)       ## Publisher initialization 
        velocity = Twist()
        while True:    
            rospy.loginfo("What kind of motion are we looking for ? 1.Linear Motion 2.Angular Motion 3.Go_to_goal motion")
            
            user_input = str(input())

            if user_input == '1':
                rospy.loginfo("enter the linear velocity less than 0.4" )     ## Input Velocity
                vel = float(input())
                rospy.loginfo("enter the distance to be covered")       ## Input Distance 
                dist = float(input())
                rospy.loginfo("enter the direction to be covered 1 for forward 0 for reverse")      ## Input the direction Forward or Reverse
                direct = int(input())
                linear_move(vel,dist,direct)         ## Function call for linear motion
            
            elif user_input=='2':
                print("enter the angular velocity")  ## Input Angular Velocity
                angular_speed = float(input())
                print("enter the angle to be rotated") ## Angle for rotation to take place
                angle_of_rotation = float(input())
                print("Clock-wise(0) or Anti-Clockwise(1)") ##Direction of Rotation 
                rotation_side = int(input())
                rotation_move(angular_speed,angle_of_rotation,rotation_side) ## Function call for rotational motion

            elif user_input == '3':
                print("enter goal location: X Coordinate :")        ## X-Coordinate of goal
                x_coordinate = float(input())
                print("enter the Y coordinate :")           ## Y-Coordinate of goal 
                y_coordinate = float(input())
                go_to_goal(x_coordinate,y_coordinate)   ## Function call to go to goal
            
            else:
                print("Invalid Entry! Try Once again!")
        
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")





        
               
        
        

        


        


        
        
        

        
    
