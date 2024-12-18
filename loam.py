#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import csv
import matplotlib.pyplot as plt
import numpy as np


class OdometryRecorder:
    def __init__(self):
        self.data_file = "odometry_data.csv"
        rospy.init_node("odometry_recorder", anonymous=True)
        self.subscriber = rospy.Subscriber("/aft_mapped_to_init_high_frec", Odometry, self.callback)
        self.file_initialized = False
        rospy.loginfo("Subscribed to /odometry topic")

    def callback(self, msg):
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        if not self.file_initialized:
            with open(self.data_file, "w") as file:
                writer = csv.writer(file)
                writer.writerow(["Time", "X", "Y", "Z", "Orientation_X", "Orientation_Y", "Orientation_Z", "Orientation_W"])
            self.file_initialized = True

        with open(self.data_file, "a") as file:
            writer = csv.writer(file)
            writer.writerow([
                rospy.Time.now().to_sec(),
                position.x, position.y, position.z,
                orientation.x, orientation.y, orientation.z, orientation.w
            ])

    def run(self):
        rospy.spin()


def read_and_plot(file_name):
    # Load data
    data = np.genfromtxt(file_name, delimiter=',', skip_header=1, names=True)
    # time = data['Time']
    x = data['X']
    y = data['Y']

    # Plot trajectory
    plt.figure()
    plt.plot(x, y, label="Trajectory")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.title("Robot Trajectory")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    try:
        # Run the odometry recorder
        recorder = OdometryRecorder()
        rospy.loginfo("Recording odometry data...")
        recorder.run()

    except rospy.ROSInterruptException:
        pass

    # Once the recording is stopped, read the file and plot the results
    try:
        rospy.loginfo("Reading odometry data and plotting results...")
        read_and_plot("/home/ali/fastlio/odometry_data.csv")
    except Exception as e:
        rospy.logerr(f"Failed to read and plot data: {e}")
