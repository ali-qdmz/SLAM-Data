import random
from time import time
# from tkinter import E
import pandas as pd
import os
import math
from sklearn.metrics import mean_squared_error 
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.transforms import Affine2D
import math
from sklearn.metrics import mean_squared_error 


dir = "/home/ali/bagfiles (copy)"


df_odom = pd.read_csv(dir + "/orb_slam_2_final/_slash_orb_slam2_mono_slash_pose.csv")
df_gt = pd.read_csv(dir + "/orb_slam_2_final/_slash_lio_sam_slash_mapping_slash_odometry.csv")



class GT_points():
    
    def __init__(self, df):
        self.dataframe = df
        self.x = df['x']
        self.y = df['y']
        self.z = df['z']
        self.x_1 = df['x.1']
        self.y_1 = df['y.1']
        self.z_1 = df['z.1']
        self.curve = []
        for i in range(len(df)):
            self.curve.append([df['x'][i], df['y'][i]])
    
    def update_curve(self):
        self.curve= []
        for i in range(len(self.x)):
            self.curve.append([self.x[i], self.y[i]])

class Odom_points():
    
    def __init__(self, df):

        self.dataframe = df
        self.x = df['x']
        self.y = df['y']
        self.z = df['z']
        self.x_1 = df['x.1']
        self.y_1 = df['y.1']
        self.z_1 = df['z.1']
        self.curve = []
        # for i in range(len(self.x)):
        #     self.x[i] = -1 * self.x[i]

        for i in range(len(df)):
            self.curve.append([df['x'][i], df['y'][i]])

    def update_curve(self):
        self.curve = []
        for i in range(len(self.x)):
            self.curve.append([self.x[i], self.y[i]])

    def scale_shift_rotate(self, scale, shift_x, shift_y, rotate):
        deg = rotate * math.pi/180
        rotation_matirx = np.array([[math.cos(deg), -math.sin(deg), 0],
                                    [math.sin(deg), math.cos(deg), 0],
                                    [0, 0, 1]])
        #scaling
        self.x = (self.x * scale)
        self.y = (self.y * scale)

        #rotating points
        points = []
        for i in range(len(self.x)):
            new_p = np.dot(np.array([self.x[i], self.y[i], 0]), rotation_matirx)
            points.append(new_p)

        points = np.array(points)
        self.x = points[:, 0]
        self.y = points[:, 1]

        #rotating orientation (testing)
        points = []
        for i in range(len(self.x_1)):
            new_p = np.dot([self.x_1[i], self.y_1[i], 0], rotation_matirx)
            points.append(new_p)

        points = np.array(points)
        self.x_1 = points[:, 0]
        self.y_1 = points[:, 1]

        #shifting points
        self.x = self.x + shift_x
        self.y = self.y + shift_y

        self.update_curve()


    def match_counter_points(self, gt_object):
        self.update_curve()
        gt_object.update_curve()
        if len(self.curve) > len(gt_object.curve):
            print("if")
            points = []
            orientations = []
            for i in range(225, len(gt_object.curve)):
                distances = []
                indexes_positions = []
                indexes_orientations = []
                for j in range(len(self.curve)):
                    distance = math.sqrt((gt_object.curve[i][0] - self.curve[j][0])**2 + (gt_object.curve[i][1] - self.curve[j][1])**2)
                    distances.append(distance)
                    indexes_positions.append([self.curve[j][0], self.curve[j][1]])
                    indexes_orientations.append([self.z_1[j]])
                counter_point = indexes_positions[distances.index(min(distances))]
                counter_orientation = indexes_orientations[distances.index(min(distances))]
                points.append([[gt_object.curve[i][0], gt_object.curve[i][1]], counter_point])
                orientations.append([[gt_object.z_1[i]], counter_orientation])

            points = np.array(points)
            gt_object.x = points[:, 0, 0]
            self.x = points[:, 1, 0]
            gt_object.y = points[:, 0, 1]
            self.y = points[:, 1, 1]

            orientations = np.array(orientations)
            gt_object.z_1 = orientations[:, 0]
            self.z_1 = orientations[:, 1]
            # gt_object.y_1 = orientations[:, 0, 1]
            # self.y_1 = orientations[:, 1, 1]

            self.update_curve()

        else:
            print("This is else! your are fucked up.")
            points = []
            for i in range(len(self.curve)):
                distances = []
                indexes_positions = []
                for j in range(len(gt_object.curve)):
                    distance = math.sqrt((self.curve[i][0] - gt_object.curve[j][0])**2 + (self.curve[i][1] - gt_object.curve[j][1])**2)
                    distances.append(distance)
                    indexes_positions.append([gt_object.curve[j][0], gt_object.curve[j][1]])
                counter_point = indexes_positions[distances.index(min(distances))]
                points.append([[self.curve[i][0], self.curve[i][1]], counter_point])
            points = np.array(points)
            self.x = points[:, 0, 0]
            gt_object.x = points[:, 1, 0]
            self.y = points[:, 0, 1]
            gt_object.y = points[:, 1, 1]
            self.update_curve()

    def caclulate_rmse(self, gt_object):
        mse = mean_squared_error(np.array([self.x, self.y]), np.array([gt_object.x, gt_object.y]))
        print(mse)


def plot(x, y):
    plt.plot(x, y)
    plt.xlabel('Meters')
    plt.ylabel('Meters')
    plt.show()

def plot_all(gt_obj, odom_obj):
    plt.plot(gt_obj.x, gt_obj.y)
    plt.plot(odom_obj.x, odom_obj.y)
    plt.xlabel('Meters')
    plt.ylabel('Meters')
    plt.show()



def plot_errors(odom_object, ground_truth_object):
    errors = []
    for i in range(len(odom_object.x)):
        error = math.sqrt((odom_object.x[i] - ground_truth_object.x[i])**2 + (odom_object.y[i] - ground_truth_object.y[i])**2)
        errors.append(error)

    plt.plot(errors)
    plt.show()

    errors = []
    for i in range(len(odom_object.x)):
        error = odom_object.z_1[i] - ground_truth_object.z_1[i]
        errors.append(error)

    plt.plot(errors)
    plt.show()


odom_object = Odom_points(df=df_odom)
ground_truth_object = GT_points(df=df_gt)

shift_x = ground_truth_object.x[225] - odom_object.x[0]
shift_y = ground_truth_object.y[225] - odom_object.x[0]

odom_object.scale_shift_rotate(scale=5.5, shift_x=shift_x,shift_y=shift_y,rotate=45)
plot_all(odom_obj=odom_object,gt_obj=ground_truth_object)

odom_object.match_counter_points(ground_truth_object)
odom_object.caclulate_rmse(ground_truth_object)

plot_errors(odom_object=odom_object, ground_truth_object=ground_truth_object)
plot_all(odom_obj=odom_object,gt_obj=ground_truth_object)
