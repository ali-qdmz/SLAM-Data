#!/usr/bin/env python

import rospy
import csv
import matplotlib.pyplot as plt
from nav_msgs.msg import Path


class PathRecorder:
    def __init__(self):
        self.file_name = "aft_mapped_path.csv"

        # Initialize ROS node
        rospy.init_node("path_recorder", anonymous=True)

        # Subscribe to the path topic
        rospy.Subscriber("/aft_mapped_path", Path, self.path_callback)

        # Initialize the CSV file
        with open(self.file_name, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Time", "X", "Y", "Z"])
        rospy.loginfo("Recording data from /aft_mapped_path")

    def path_callback(self, msg):
        timestamp = rospy.Time.now().to_sec()
        with open(self.file_name, "a") as file:
            writer = csv.writer(file)
            for pose_stamped in msg.poses:  # Each PoseStamped object in the Path message
                position = pose_stamped.pose.position
                writer.writerow([
                    timestamp,
                    position.x, position.y, position.z
                ])

    def run(self):
        rospy.spin()


def visualize_path(file_name):
    # Load the data from the CSV file
    x_positions = []
    y_positions = []

    with open(file_name, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            x_positions.append(float(row["X"]))
            y_positions.append(float(row["Y"]))

    # Plot the path
    plt.figure()
    plt.scatter(x_positions, y_positions, label="Path Trajectory")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.title("Path Trajectory Visualization")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    try:
        # Start recording path data
        recorder = PathRecorder()
        rospy.loginfo("Recording path data. Press Ctrl+C to stop.")
        recorder.run()

    except rospy.ROSInterruptException:
        pass

    # Visualize the path once recording is complete
    try:
        rospy.loginfo("Reading recorded data and visualizing the path...")
        visualize_path("aft_mapped_path.csv")
    except Exception as e:
        rospy.logerr(f"Failed to visualize data: {e}")
