#!/usr/bin/env python3
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt, pi
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler


class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_goal', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/odom', Odometry, self.update_pose)
        
    	#def callback(msg):
        #print(msg.pose.pose)
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.theta = 0

        self.pose = Odometry()
        self.pose_position = self.pose.pose.pose.position
        self.pose_orientation = self.pose.pose.pose.orientation
        self.rate = rospy.Rate(10)
    
    def get_rotation(self):
        orientation_q = self.pose.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
        #quat = quaternion_from_euler (roll, pitch,yaw)
        #print("yaw is : ")
        #print(yaw)
        return yaw
		#print yaw

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        
        self.pose_position.x = self.pose.pose.pose.position.x
        self.pose_position.y = self.pose.pose.pose.position.y
        #self.pose_orientation.z = self.pose.pose.orientation.z
        
        self.pose_position.x = round(self.pose_position.x, 4)
        self.pose_position.y = round(self.pose_position.y, 4)
        
        self.theta = self.get_rotation()*180/pi

    def euclidean_distance(self, goal_pose_position):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose_position.x - self.pose_position.x), 2) +
                    pow((goal_pose_position.y - self.pose_position.y), 2))

    def linear_vel(self, goal_pose_position, constant=1.5):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * self.euclidean_distance(goal_pose_position)

    def steering_angle(self, goal_pose_position):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        #print("stearing angle")
        #print(atan2(goal_pose_position.y - self.pose_position.y, goal_pose_position.x - self.pose_position.x))
        return atan2(goal_pose_position.y - self.pose_position.y, goal_pose_position.x - self.pose_position.x)


    def angular_vel(self, goal_pose_position, constant=3):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * (self.steering_angle(goal_pose_position) - self.theta*pi/180)

    def move2goal(self, point_x, point_y):
        """Moves the turtle to the goal."""
        #goal_pose = self.pose.pose.pose.position
        goal_pose = Odometry()

        # Get the input from the user.
        #goal_pose.pose.pose.position.x = float(input("Set your x goal: "))
        #goal_pose.pose.pose.position.y = float(input("Set your y goal: "))
        goal_pose.pose.pose.position.x = float(point_x)
        goal_pose.pose.pose.position.y = float(point_y)
        print(self.pose_position)
        print(goal_pose)

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        #distance_tolerance = float(input("Set your tolerance: "))
        distance_tolerance = float(0.2)

        vel_msg = Twist()
        #vel_msg.linear.x = goal_pose.pose.pose.position.x
        #vel_msg.linear.y = goal_pose.pose.pose.position.y
        #print(vel_msg)
        
        # stering angle
        #angle = self.steering_angle(goal_pose.pose.pose.position)
        #print("steering angle is: ")
        #print(angle)
        
        #angle_deg = 
        

        while self.euclidean_distance(goal_pose.pose.pose.position) >= distance_tolerance:
        #while(False):

            # Porportional controller.
            # https://en.wikipedia.org/wiki/Proportional_control

            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose.pose.pose.position)/10
            #vel_msg.linear.x = goal_pose.pose.pose.position.x
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose.pose.pose.position)/1
            #vel_msg.angular.z = 0
            print(self.angular_vel(goal_pose.pose.pose.position)/100)
            print(self.pose_position.x)
            print(self.pose_position.y)
            print(pi)
            print(self.theta)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        #rospy.spin()

if __name__ == '__main__':

	list_points = []
	list_points.append([1,3])
	list_points.append([1,6])
	list_points.append([6,6])
	list_points.append([6,2])
	x = TurtleBot()
	for i in list_points:
		try:
		    x.move2goal(i[0], i[1])
		except rospy.ROSInterruptException:
		    pass
