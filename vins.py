#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped
import csv
import matplotlib.pyplot as plt
import numpy as np


class MultiTopicRecorder:
    def __init__(self):
        # Filenames for saving data
        self.odom_file = "vins_estimator_odometry.csv"
        self.path_file = "pose_graph_path.csv"

        # Initialize node
        rospy.init_node("multi_topic_recorder", anonymous=True)

        # Subscribers
        rospy.Subscriber("/vins_estimator/odometry", Odometry, self.odom_callback)
        rospy.Subscriber("/pose_graph/pose_graph_path", Path, self.path_callback)

        # Initialize files
        self.init_file(self.odom_file, ["Time", "X", "Y", "Z", "Orientation_X", "Orientation_Y", "Orientation_Z", "Orientation_W"])
        self.init_file(self.path_file, ["Time", "X", "Y", "Z"])

        rospy.loginfo("Subscribed to /vins_estimator/odometry and /pose_graph/pose_graph_path")

    def init_file(self, file_name, headers):
        with open(file_name, "w") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    def odom_callback(self, msg):
        # Extract odometry data
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation

        # Write data to file
        with open(self.odom_file, "a") as file:
            writer = csv.writer(file)
            writer.writerow([
                rospy.Time.now().to_sec(),
                position.x, position.y, position.z,
                orientation.x, orientation.y, orientation.z, orientation.w
            ])

    def path_callback(self, msg):
        # Extract path data
        timestamp = rospy.Time.now().to_sec()
        for pose in msg.poses:
            position = pose.pose.position
            with open(self.path_file, "a") as file:
                writer = csv.writer(file)
                writer.writerow([
                    timestamp,
                    position.x, position.y, position.z
                ])

    def run(self):
        rospy.spin()


def read_and_plot(odom_file, path_file):
    # Load odometry data
    odom_data = np.genfromtxt(odom_file, delimiter=',', skip_header=1, names=True)
    odom_x = odom_data['X']
    odom_y = odom_data['Y']

    # Load path data
    path_data = np.genfromtxt(path_file, delimiter=',', skip_header=1, names=True)
    path_x = path_data['X']
    path_y = path_data['Y']

    # Plot odometry trajectory
    plt.figure()
    plt.plot(odom_x, odom_y, label="Odometry Trajectory (/vins_estimator/odometry)")
    # plt.plot(path_x, path_y, label="Path Trajectory (/pose_graph/pose_graph_path)")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.title("Trajectories from Odometry and Path")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    # try:
    #     # Run the multi-topic recorder
    #     recorder = MultiTopicRecorder()
    #     rospy.loginfo("Recording odometry and path data...")
    #     recorder.run()

    # except rospy.ROSInterruptException:
    #     pass

    # Once the recording is stopped, read the files and plot the results
    try:
        rospy.loginfo("Reading data and plotting results...")
        read_and_plot("vins_estimator_odometry.csv", "pose_graph_path.csv")
    except Exception as e:
        rospy.logerr(f"Failed to read and plot data: {e}")
