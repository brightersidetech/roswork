#!/usr/bin/env python3
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt, pi
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler


#orientation_q = self.pose.pose.pose.orientation
orientation_list = [-0.002705935486205009, 0.0027453138363401778, 0.7009084193343534, 0.7132408631530466]
(roll, pitch, yaw) = euler_from_quaternion (orientation_list)
print(yaw*180/pi)
        #quat = quaternion_from_euler (roll, pitch,yaw)
        #print("yaw is : ")
        #print(yaw)
        #return yaw
		#print yaw
