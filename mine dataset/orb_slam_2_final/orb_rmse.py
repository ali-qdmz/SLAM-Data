import random
from time import time
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


df_odom = pd.read_csv("/home/ali/bagfiles (copy)/orb_slam_2/_slash_orb_slam2_mono_slash_pose.csv")
df_gt = pd.read_csv("/home/ali/bagfiles (copy)/LIO_final/_slash_lio_sam_slash_mapping_slash_odometry.csv")




def minimum_rmse_angle(deg, scale, df_gt, df_odom):
    deg = deg * math.pi/180
    rotation_matirx = np.array([[math.cos(deg), -math.sin(deg), 0],
                                [math.sin(deg), math.cos(deg), 0],
                                [0, 0, 1]])

    x_gt = df_gt['x'] 
    y_gt = df_gt['y']
    z_gt = df_gt['z']
    x_odom = (df_odom['x'] * scale)
    y_odom = (df_odom['y'] * scale)
    z_odom = df_odom['z']

    points = []
    for i in range(len(x_odom)):
        new_p = np.dot([x_odom[i], y_odom[i], 0], rotation_matirx)
        points.append(new_p)

    points = np.array(points)
    x_odom = points[:, 0]
    y_odom = points[:, 1]

    x_bias = x_gt[225] - x_odom[0]
    y_bias = y_gt[225] - y_odom[0]
    # x_bias = 0
    # print(x_bias, y_bias)
    x_odom = x_odom + x_bias
    y_odom = y_odom + y_bias
    z_odom = df_odom['z']


    slicer = min(len(x_odom), len(x_gt))
    mse = mean_squared_error(np.array([x_gt[:slicer], y_gt[:slicer]]), np.array([x_odom[:slicer], y_odom[:slicer]]))
    return mse, x_odom, y_odom, x_gt, y_gt


def find_nearest_point(curve1, curve2):
    
    if len(curve1) > len(curve2):
        points = []
        for i in range(225,len(curve2)):
            distances = []
            indexes = []
            for j in range(len(curve1)):
                distance = math.sqrt((curve2[i][0] - curve1[j][0])**2 + (curve2[i][1] - curve1[j][1])**2)
                distances.append(distance)
                indexes.append([curve1[j][0], curve1[j][1]])
            counter_point = indexes[distances.index(min(distances))]
            points.append([[curve2[i][0], curve2[i][1]], counter_point])
    
    else:
        points = []
        for i in range(len(curve1)):
            distances = []
            indexes = []
            for j in range(len(curve2)):
                distance = math.sqrt((curve1[i][0] - curve2[j][0])**2 + (curve1[i][1] - curve2[j][1])**2)
                distances.append(distance)
                indexes.append([curve2[j][0], curve2[j][1]])
            counter_point = indexes[distances.index(min(distances))]
            points.append([[curve1[i][0], curve1[i][1]], counter_point])
    points = np.array(points)
    x_1 = points[:, 0, 0]
    x_2 = points[:, 1, 0]
    y_1 = points[:, 0, 1]
    y_2 = points[:, 1, 1]
    mse = mean_squared_error(np.array([x_1, y_1]), np.array([x_2, y_2]))
    print(mse)
    return points


# mses = []
# plots = []
# for i in range(1, 360):
#     mse, x_odom, y_odom, x_gt, y_gt = minimum_rmse_angle(i, scale=5.5, df_odom=df_odom, df_gt=df_gt)
#     mses.append(mse)
#     plots.append([x_odom, y_odom, x_gt, y_gt])
# index = mses.index(min(mses))
# print(min(mses))

def main():
    mse, x_odom, y_odom, x_gt, y_gt = minimum_rmse_angle(40, scale=1, df_odom=df_odom, df_gt=df_gt)
    curve1 = []
    for i in range(len(x_odom)):
        curve1.append([x_odom[i], y_odom[i]])
    curve2 = []
    for i in range(len(x_gt)):
        curve2.append([x_gt[i], y_gt[i]])

    points = find_nearest_point(curve1=curve1, curve2=curve2)
    points = np.array(points)

    x_1 = points[:, 0, 0]
    x_2 = points[:, 1, 0]
    y_1 = points[:, 0, 1]
    y_2 = points[:, 1, 1]

    # print(points.shape)
    # print(points[10][0][0], x_1[10])

    # x_odom = plots[index][0]
    # y_odom = plots[index][1]
    # x_gt = plots[index][2]
    # y_gt = plots[index][3]

    # plt.plot(x_1, y_1)
    plt.plot(x_1, y_1)
    plt.plot(x_2, y_2)
    # plt.scatter(x_gt[225],y_gt[225])
    plt.xlabel('Meters')
    plt.ylabel('Meters')
    plt.show()

    # x_odom = x_1
    # x_gt = x_2
    # y_odom = y_1
    # y_gt = y_2
    errors = []
    for i in range(min(len(x_odom), len(x_gt))):
        error = math.sqrt((x_odom[i] - x_gt[i])**2 + (y_odom[i] - y_gt[i])**2)
        errors.append(error)


    plt.plot(errors)
    plt.show()

def plot(x, y):
    plt.plot(x, y)
    plt.xlabel('Meters')
    plt.ylabel('Meters')
    plt.show()

main()
plot(df_odom['x'], df_odom['y'])