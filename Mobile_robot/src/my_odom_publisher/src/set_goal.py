#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

import math
from math import sin, cos, pi



def movebase_client():
    t = 0
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    cur_time = rospy.Time.now().to_sec()

    for i in range(0, 72):

        rad = t*3.14/180

        goal.target_pose.pose.position.x = 3*sin(rad)
        goal.target_pose.pose.position.y = 3*cos(rad)
        goal.target_pose.pose.orientation.z = 0.5
        goal.target_pose.pose.orientation.w = 1.0

        print(goal.target_pose.pose.position.x)

        client.send_goal(goal)
        wait = client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            t += 5
            


if __name__ == '__main__':

    try:
        rospy.init_node('movebase_client_py')

        result = movebase_client()

        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")