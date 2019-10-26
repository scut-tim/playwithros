#include<ros/ros.h>
#include<geometry_msgs/Twist.h>
#include<cmath>
#include"turtlesim/Pose.h"
#include<std_srvs/Empty.h>
#include<iostream>
#include<algorithm>

using namespace std;


class collect_max_coins{
    
public:

    int matrix[6][7];//6x7 simplify
    int* a[6];
    struct position
    {
        int x,y;
        /* data */
    }positions[100];
    
    int pindex;

    collect_max_coins(){
        for(int i = 0;i<6;i++){
            for(int j = 0;j<7;j++)matrix[i][j] = 0;
        }
    }

    void fill_table(int* a[]){
        for(int i = 1;i<6;i++){
            for(int j = 1;j<7;j++){
                int max = matrix[i-1][j] > matrix[i][j-1] ? matrix[i-1][j] : matrix[i][j-1];

                matrix[i][j] = max + a[i][j];
            }
        }   
        
        for(int i = 0;i<6;i++){
            for(int j = 0;j<7;j++)cout<<matrix[i][j]<<" ";
            cout<<endl;
        }
        
    }

    void get_coins_distr(){
        int pos;
        
        for(int i = 0;i<7;i++)a[i] = new int[7]; 
        for(int i = 0;i<6;i++){
            for(int j = 0;j<7;j++){
                cin>>pos;
                a[i][j] = pos;
            }
        }cout<<endl;
        fill_table(a);
    }

    static int cmp1(position a,position b){
        if(a.y != b.y)return a.y>b.y;
        return a.x<b.x;
    }

    // int cmp2(position a,position b){
    //     return a.y<b.y;
    // }



    void get_path(){
        int i = 5;
        int j = 6;
        pindex = 0;
        position p; 
        // p.x = 1; p.y = 6-1;
        // positions[pindex++] = p;
        while(true){
            p.x = j; p.y = 6-i;
            positions[pindex++] = p;
           
            if(i == 1)j--;
            else if(j == 1)i--;
            else if(matrix[i-1][j]>matrix[i][j-1]) i--;
            else j--;

            if(i == 0 || j == 0)break;
                    
            
                    
                
        }
        // p.x = j;p.y =6-i;
        // positions[pindex++] = p;

        sort(positions,positions+pindex,cmp1);

        for(int i = 0;i<pindex;i++){
            cout<<positions[i].x<<" "<<positions[i].y<<endl;
        }

    }
    
        

};

turtlesim::Pose* p = new turtlesim::Pose();

void poseCallback(const turtlesim::Pose::ConstPtr& msg){

        

    p->x = msg->x;
    p->y = msg->y;

            



}

int main(int argc, char **argv)
{
    ros::init(argc,argv,"goal_pub");
    ros::NodeHandle n;
    collect_max_coins c;
    ros::Publisher goal_pub = n.advertise<turtlesim::Pose>("/goal_info",10);
    ros::Subscriber pose_sub = n.subscribe("/turtle1/pose",10,poseCallback);
    
    ros::service::waitForService("/clear");
    ros::ServiceClient clin = n.serviceClient<std_srvs::Empty>("/clear");
    
    std_srvs::Empty srv;

    ros::Rate loop_rate(1);
    loop_rate.sleep();
    ros::spinOnce();
    
    
    
    
    
    
    c.get_coins_distr();
    c.get_path();
    
    

    
        turtlesim::Pose goal_info;
        
        
        for(int i = 0;i<c.pindex && ros::ok();i++){
            ros::spinOnce();
            

            int x = c.positions[i].x;
            int y = c.positions[i].y;
            goal_info.x = x;
            goal_info.y = y;
            
            

            double xm = p->x - x;
            double ym = p->y - y;
            double distance = sqrt(xm*xm+ym*ym);

            while(distance >= 0.02 && ros::ok){

                goal_pub.publish(goal_info);
                
                
                ros::spinOnce();
                
                xm = p->x - x;
                ym = p->y - y;
                distance = sqrt(xm*xm+ym*ym);
            }

            if(x == 1 && y == 5)clin.call(srv);
            c.a[6-y][x] = 8;
            for(int i = 0;i<6;i++){
                for(int j = 0;j<7;j++)cout<<c.a[i][j]<<" ";
                cout<<endl;
            }
            cout<<endl;


            loop_rate.sleep();

            
        }
    

        
    
}