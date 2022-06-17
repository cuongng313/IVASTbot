#!/usr/bin/env python

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import  TwistStamped, Pose, Point, Vector3, Quaternion
from std_msgs.msg import Header, ColorRGBA, String
from nav_msgs.msg import Odometry




class TrajectoryInteractiveMarkers:
    def __init__(self):
        self.count = 0
        # rospy.Subscriber("/arm_1/arm_controller/cartesian_velocity_command", TwistStamped, self.event_in_cb)
        rospy.Subscriber("/odom", Odometry, self.event_in_cb)
        rospy.sleep(1)


    def event_in_cb(self, msg):
        self.waypoints = msg
        # self.a = [1, 1, 1]
        self.a = list()
        self.a.append(self.waypoints.twist.twist.linear.x)
        self.a.append(self.waypoints.twist.twist.linear.y)
        self.a.append(self.waypoints.twist.twist.angular.z)
        self.show_text_in_rviz()


    def show_text_in_rviz(self):
        self.marker = Marker()
        self.marker_publisher = rospy.Publisher('visualization_marker', Marker, queue_size=50)
        self.marker = Marker(
            type=Marker.CUBE,
            id=0,
            lifetime=rospy.Duration(10000000),
            pose=Pose(Point(self.a[0] / 10 ** 5, self.a[1] / 10 ** 5, self.a[2] / 10 ** 5), Quaternion(0, 0, 0, 1)),
            scale=Vector3(0.25, 0.25, 0.0001),
            header=Header(frame_id='base_footprint'),
            color=ColorRGBA(250.0, 0.0, 0.0, 0.8))
        self.count += 1
        self.marker.id = self.count
        self.marker_publisher.publish(self.marker)




if __name__ == '__main__':
    rospy.init_node("trajectory_interactive_markers_node", anonymous=True)
    trajectory_interactive_markers = TrajectoryInteractiveMarkers()

    rospy.sleep(1)
    rospy.spin()