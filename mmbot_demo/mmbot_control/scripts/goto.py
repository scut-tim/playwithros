#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from math import pow, atan2, sqrt
import tf
from tf.transformations import euler_from_quaternion




    #rospy.init_node("goto",anonymous=True)

class Mmbot:

    def __init__(self):
        

        rospy.init_node('goto',anonymous=True)

        self.velocity_publisher = rospy.Publisher('cmd_vel',Twist,queue_size=5)

        self.pose_subscriber = rospy.Subscriber('/odom',Odometry,self.update_pose)
        
        self.odometry = Odometry()

        self.rate = rospy.Rate(20)

    def update_pose(self,data):

        self.odometry = data
        self.odometry.pose.pose.position.x = round(self.odometry.pose.pose.position.x,4)
        self.odometry.pose.pose.position.y = round(self.odometry.pose.pose.position.y,4)
        #self.odometry.pose.pose.position.x = data.pose.pose.position.x
        #self.odometry.pose.pose.position.y = data.pose.pose.position.y

    def euclidean_distance(self,goal_pose):

        return sqrt(pow((goal_pose.pose.pose.position.x - self.odometry.pose.pose.position.x), 2) +
                    pow((goal_pose. pose.pose.position.y- self.odometry.pose.pose.position.y), 2))
    
    def linear_vel(self, goal_pose, constant=1.5):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return atan2(goal_pose.pose.pose.position.y - self.odometry.pose.pose.position.y, goal_pose.pose.pose.position.x - self.odometry.pose.pose.position.x)

    def angular_vel(self, goal_pose, constant=6):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        
        p = euler_from_quaternion((self.odometry.pose.pose.orientation.x,
                                   self.odometry.pose.pose.orientation.y,
                                    self.odometry.pose.pose.orientation.z,
                                    self.odometry.pose.pose.orientation.w))
        
        
        return constant * (self.steering_angle(goal_pose) - p[2])


    def move2goal(self):
        self.rate.sleep()
        """Moves the turtle to the goal."""
        goal_pose = Odometry()

        # Get the input from the user.
        goal_pose.pose.pose.position.x = input("Set your x goal: ")
        goal_pose.pose.pose.position.y = input("Set your y goal: ")

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = input("Set your tolerance: ")

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= distance_tolerance:

            # Porportional controller.
            # https://en.wikipedia.org/wiki/Proportional_control

            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            rospy.loginfo(">>>>>???<<<<<<<")

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

if __name__ == '__main__':
    try:
        x = Mmbot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass

