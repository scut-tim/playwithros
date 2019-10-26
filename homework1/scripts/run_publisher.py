#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist

def twist_publisher():
    rospy.init_node('twist_publisher', anonymous=True)

    turtle_vel_pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=100)

    rate = rospy.Rate(0.5)

    rate.sleep()
    while not rospy.is_shutdown():
        for i in range(4):
            vel_msg1 = Twist()
            vel_msg1.linear.x = 2
            
            
            turtle_vel_pub.publish(vel_msg1)
            rospy.loginfo("vel_msg1: %0.2f",vel_msg1.linear.x)
            vel_msg2 = Twist()
            vel_msg2.angular.z = math.pi/2
            if i < 3:
                rate.sleep()
                turtle_vel_pub.publish(vel_msg2)

            rospy.loginfo('py')
            rate.sleep()
        
        vel_msg3 = Twist()
        vel_msg3.linear.x = 10
        vel_msg3.angular.z = math.pi*2
        turtle_vel_pub.publish(vel_msg3)
        rate.sleep()
        

if __name__ == '__main__':
    try:
        twist_publisher()
    except rospy.ROSInterruptException:
        pass
        