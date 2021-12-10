#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def get_sign(x):
	if(x<0):
		return -1;
	else:
		return 1

def move():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    #Receiveing the user's input
    #print("Let's move your robot")
    #speed = int(input("Input your speed:"))
    #distance = int(input("Type your distance:"))
    #isForward = input("Foward?: ")#True or False

    #Checking if the movement is forward or backwards
    #if(isForward):
    #   vel_msg.linear.x = abs(speed)
    #else:
     #   vel_msg.linear.x = -abs(speed)
    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    while not rospy.is_shutdown():
    
    	   #Receiveing the user's input
    	print("Let's move your robot")
    	x_distance = int(input("Input your x distance:"))
    	#isForward_x = int(input("Foward in x?: "))
    	isForward_x = get_sign(x_distance)
    	y_distance = int(input("Type your y distance:"))
    	#isForward_y = int(input("Foward in y?: "))#True or False
    	isForward_y = get_sign(y_distance)
    	
    	rotate_z = 0
    	
    	
    	if(x_distance == 0 and y_distance == 0):
    		rotate_z = 0
    	if(x_distance == 0 and y_distance !=0):
    		rotate_z = get_sign(y_distance)*0.8
    	if(x_distance != 0 and y_distance == 0):
    		rotate_z = 0
    	if(x_distance!=0 and y_distance!= 0):
    		rotate_z = get_sign(y_distance)*0.8
    		

    	#Checking if the movement is forward or backwards
    	if(isForward_x==1):
    		vel_msg.linear.x = abs(0.2)
    	else:
    		vel_msg.linear.x = -abs(0.2)
    	
    	#Since we are moving just in x-axis
    	vel_msg.linear.y = 0
    	vel_msg.linear.z = 0
    	vel_msg.angular.x = 0
    	vel_msg.angular.y = 0
    	vel_msg.angular.z = 0
    	
    	#Setting the current time for distance calculus
    	t0 = rospy.Time.now().to_sec()
    	current_distance = 0
    	
    	#Loop to move the turtle in an specified distance
    	while(current_distance < abs(x_distance)):
    		#Publish the velocity
    		velocity_publisher.publish(vel_msg)
    		#Takes actual time to velocity calculus
    		t1=rospy.Time.now().to_sec()
    		#Calculates distancePoseStamped
    		current_distance= 1*(t1-t0)
    		
    	#After the loop, stops the robot
    	vel_msg.linear.x = 0
    	#Force the robot to stop
    	velocity_publisher.publish(vel_msg)
    	
    	
    	t0 = rospy.Time.now().to_sec()
    	t1 = rospy.Time.now().to_sec()
    	vel_msg.angular.z = rotate_z
    	while(t1 -t0 <2):
    		velocity_publisher.publish(vel_msg)
    		t1 = rospy.Time.now().to_sec()
    		
    	# stop angle
    	vel_msg.angular.z = 0
    	velocity_publisher.publish(vel_msg)
    	
    	
    	#Checking if the movement is forward or backwards
    	if(isForward_y==1):
    		vel_msg.linear.x = abs(0.2)
    	else(:
    		vel_msg.linear.x = -abs(0.2)
    	
    	#Since we are moving just in x-axis
    	vel_msg.linear.y = 0
    	vel_msg.linear.z = 0
    	vel_msg.angular.x = 0
    	vel_msg.angular.y = 0
    	vel_msg.angular.z = 0
    	
    	#Setting the current time for distance calculus
    	t0 = rospy.Time.now().to_sec()
    	current_distance = 0
    	
    	#Loop to move the turtle in an specified distance
    	while(current_distance < abs(y_distance)):
    		#Publish the velocity
    		velocity_publisher.publish(vel_msg)
    		#Takes actual time to velocity calculus
    		t1=rospy.Time.now().to_sec()
    		#Calculates distancePoseStamped
    		current_distance= 1*(t1-t0)
    		
    	#After the loop, stops the robot
    	vel_msg.linear.x = 0
    	#Force the robot to stop
    	velocity_publisher.publish(vel_msg)
    	

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
