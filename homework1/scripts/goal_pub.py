#!/usr/bin/env python
import rospy
from turtlesim.msg import Pose
from math import sqrt
from std_srvs.srv import Empty
class position:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
    

class collect_max_coins:


    def __init__(self,r,c):
        self.r = r+1
        self.c = c+1
        self.table = [[0 for i in range(c+1)] for j in range(r+1)]
        self.coins_distr = [[0 for i in range(c+1)] for j in range(r+1)]
        self.positions = []


        rospy.init_node('goal_pub',anonymous=True)

        self.goal_pub = rospy.Publisher('/goal_info',Pose,queue_size=10)
        self.pose_sub = rospy.Subscriber('/turtle1/pose',Pose,self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)

        


    def update_pose(self, data):
       
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
    
    def get_coins_distr(self):
        for i in range(self.r):
            l = raw_input()
            line = l.split(' ')
            for j in range(self.c):
                self.coins_distr[i][j] = int(line[j])
                



    def fill_table(self):
        for i in range(1,self.r):
            for j in range(1,self.c):
                if self.table[i - 1][j]>self.table[i][j-1]:
                    self.table[i][j] += self.coins_distr[i][j] + self.table[i-1][j]
                else:
                    self.table[i][j] += self.coins_distr[i][j] + self.table[i][j-1]
                    

    def show(self):
        for i in self.table:
            print(i)

    def cmp(self,p1,p2):
        if(p1.y != p2.y): return p2.y - p1.y
        else: return p1.x - p2.x


    def get_path(self):
        i = self.r - 1
        j = self.c - 1
        while(j != 0 and i != 0):
            
            p = position(j,self.r - i)
            
            self.positions.append(p)

            if j == 1: i = i - 1
                
            elif i == 1: j =j - 1
                
            elif self.table[i-1][j]>self.table[i][j-1]: i = i - 1

            else: j = j - 1

        self.positions = sorted(self.positions,cmp=self.cmp)

        for i in self.positions:
            print("x: ",i.x," y: ",i.y)
                
    def start(self):

        pose = Pose()
        rospy.wait_for_service('/clear')
        clin = rospy.ServiceProxy('/clear',Empty)
        for p in self.positions:
            pose.x = p.x
            pose.y = p.y
            mx = self.pose.x - p.x
            my = self.pose.y - p.y
            distance = sqrt(mx*mx + my*my)

            while distance>0.02 and not rospy.is_shutdown():
                self.goal_pub.publish(pose)
                mx = self.pose.x - p.x
                my = self.pose.y - p.y
                distance = sqrt(mx*mx + my*my)
        
            if p.x == 1 and p.y == 5 : clin()
            
            self.coins_distr[self.r - p.y][p.x] = 8
            for i in self.coins_distr:
                print(i)
            
        

        self.rate.sleep()

            

            



if __name__ == "__main__":
    c = collect_max_coins(5,6)
    c.get_coins_distr()
    c.fill_table()
    
    c.get_path()
    c.start()
    
    pass

