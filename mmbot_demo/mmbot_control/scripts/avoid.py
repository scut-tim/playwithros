#!/usr/bin/env python


import rospy

from geometry_msgs.msg import Twist

from sensor_msgs.msg import LaserScan

import math

class Mmbot:

    def __init__(self):
        

        rospy.init_node('run_avoid',anonymous=True)

        self.velocity_publisher = rospy.Publisher('/cmd_vel',Twist,queue_size=5)

        self.pose_subscriber = rospy.Subscriber('/scan',LaserScan,self.update_ranges)
        
        self.laser_scan = LaserScan()

        self.rate = rospy.Rate(100)

    def update_ranges(self,data):
        
        print ("???in the callback fun")
        self.laser_scan = data
        print(data.ranges[0])

    def run(self):
        rr = rospy.Rate(1)
        rr.sleep()
        vel_msg = Twist()
        vel_msg.linear.x = 0.2
        while not rospy.is_shutdown():
            r = self.laser_scan.ranges
            
            if(r[2]<1 or r[3]<1):
                vel_msg.angular.z = 2
            elif(r[7]<1 or r[6]<1):
                vel_msg.angular.z = -2
            else:
                vel_msg.angular.z = 0


            if (r[4]<1):
                vel_msg.angular.z = 2
            elif(r[5]<1):
                vel_msg.angular.z = -2
            else:
                vel_msg.angular.z = 0
            
            
            
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()


        


if __name__ == '__main__':
    try:
        m = Mmbot()
        m.run()
    except rospy.ROSInterruptException:
        pass