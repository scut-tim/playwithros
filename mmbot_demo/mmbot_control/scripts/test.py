#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist



def run():
    rospy.init_node('test')
    vel_msg = Twist()
    vel_pub = rospy.Publisher("/cmd_vel",Twist,queue_size=1000)
    vel_msg.linear.x = 0.2
    

    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        vel_pub.publish(vel_msg)

        rospy.loginfo("pub!!!!!!!!")

        rate.sleep()


if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass

