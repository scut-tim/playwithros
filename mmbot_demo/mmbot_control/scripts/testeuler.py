import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from math import pow, atan2, sqrt
import tf
from tf.transformations import euler_from_quaternion

# x: 2.14769274704e-08
#       y: -0.0148244631033
#       z: 1.54388323855e-06
#       w: 0.999890111608


def tran():
    p = euler_from_quaternion((2.14769274704e-08,-0.0148244631033,1.54388323855e-06,0.999890111608))
    print p[2]

    print atan2(10,10) - p[2]
    
tran()