#! /usr/bin/env python

import rospy
import tf
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from gazebo_msgs.srv import GetModelState, GetModelStateRequest


rospy.init_node('odom_pub')
odom_pub = rospy.Publisher ('my_odom', Odometry)
odom_broadcaster = tf.TransformBroadcaster()

rospy.wait_for_service ('/gazebo/get_model_state')
get_model_srv = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)


header = Header()
header.frame_id = '/my_odom'

model = GetModelStateRequest()
model.model_name = 'vast_robot'

current_time = rospy.Time.now()
last_time = current_time
r = rospy.Rate(10)

th = 0.0

while not rospy.is_shutdown():
	odom = Odometry()	
	
	result = get_model_srv(model)
	odom.pose.pose = result.pose
	odom.twist.twist = result.twist
	
	current_time = rospy.Time.now()
	dt = (current_time - last_time).to_sec()
	delta_th = odom.twist.twist.angular.z*dt
	th += delta_th

	
	odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)
	odom_broadcaster.sendTransform(
        (odom.pose.pose.position.x, odom.pose.pose.position.y, 0.),
        odom_quat,
        current_time,
        "base_footprint",
        "my_odom"
    	)

	header.stamp = rospy.Time.now()
	odom.header = header
        odom.child_frame_id = "base_footprint"

	odom_pub.publish (odom)
        
	#print(th)
	last_time = current_time
	r.sleep()
