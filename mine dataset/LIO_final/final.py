import random
from time import time
from typing import List
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
import matplotlib.lines as mlines
import matplotlib.patches as mpatches


dir = "/home/ali/bagfiles (copy)/LIO_final"


df_odom = pd.read_csv(dir + "/_slash_lio_sam_slash_mapping_slash_odometry.csv")
df_gt = pd.read_csv(dir + "/_slash_dwm1001_slash_tag_slash_tag_slash_position.csv")


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
        for i in range(len(self.x)):
            self.x[i] = -1 * self.x[i]

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
        #scaling points
        # self.x = self.dataframe['x'] 
        # self.y = self.dataframe['y']
        # self.z = self.dataframe['z']
        self.x = (self.x * scale)
        self.y = (self.y * scale)
        # self.z = self.z #no need z

        #rotating points
        points = []
        for i in range(len(self.x)):
            new_p = np.dot([self.x[i], self.y[i], 0], rotation_matirx)
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

    def match_counter_points(self, gt_object):
        self.update_curve()
        gt_object.update_curve()
        if len(self.curve) > len(gt_object.curve):
            print("if")
            points = []
            orientations = []
            for i in range(290):
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
            for i in range(360, len(gt_object.curve)):
                distances = []
                indexes_positions = []
                indexes_orientations = []
                for j in range(len(self.dataframe) - 500, len(self.curve)):
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
        final_data = dir + "/data"
        mse = mean_squared_error(np.array([self.x, self.y]), np.array([gt_object.x, gt_object.y]))
        try:
            df = pd.read_csv(final_data + '/results.csv')
            df['rmse'] = mse
            df.to_csv(final_data + '/results.csv')
        except:
            data = [mse, 0, 0]
            df = pd.DataFrame(columns=['rmse', 'cpu_mean', 'memory_mean'], data=[data])
            df.to_csv(final_data + '/results.csv')
        print(mse)




def add_arrow_to_line2D(
    axes, line, arrow_locs=[0.2, 0.4, 0.6, 0.8],
    arrowstyle='-|>', arrowsize=1, transform=None):

    if not isinstance(line, mlines.Line2D):
        raise ValueError("expected a matplotlib.lines.Line2D object")
    x, y = line.get_xdata(), line.get_ydata()

    arrow_kw = {
        "arrowstyle": arrowstyle,
        "mutation_scale": 10 * arrowsize,
    }

    color = line.get_color()
    use_multicolor_lines = isinstance(color, np.ndarray)
    if use_multicolor_lines:
        raise NotImplementedError("multicolor lines not supported")
    else:
        arrow_kw['color'] = color

    linewidth = line.get_linewidth()
    if isinstance(linewidth, np.ndarray):
        raise NotImplementedError("multiwidth lines not supported")
    else:
        arrow_kw['linewidth'] = linewidth

    if transform is None:
        transform = axes.transData

    arrows = []
    for loc in arrow_locs:
        s = np.cumsum(np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2))
        n = np.searchsorted(s, s[-1] * loc)
        arrow_tail = (x[n], y[n])
        arrow_head = (np.mean(x[n:n + 2]), np.mean(y[n:n + 2]))
        p = mpatches.FancyArrowPatch(
            arrow_tail, arrow_head, transform=transform,
            **arrow_kw)
        axes.add_patch(p)
        arrows.append(p)
    return arrows



def plot(x, y):
    plt.plot(x, y)
    plt.xlabel('x, [meters]')
    plt.ylabel('y, [meters]')
    plt.show()

def plot_all(gt_obj, odom_obj, match=False):
    global dir
    if match:
        trim_end = 290
        tirm_start = 360

        fig, ax = plt.subplots(1, 1)
        line, = ax.plot(odom_obj.x[:trim_end], odom_obj.y[:trim_end], 'k-')
        add_arrow_to_line2D(ax, line, arrow_locs=np.linspace(0., 1., 50),
                            arrowstyle='->')

        line, = ax.plot(odom_obj.x[tirm_start:], odom_obj.y[tirm_start:], 'k-')
        add_arrow_to_line2D(ax, line, arrow_locs=np.linspace(0., 1., 50),
                            arrowstyle='->')


        markers_on = [i for i in range(len(gt_obj.x[:trim_end])) if i%20 == 0]
        line, = ax.plot(gt_obj.x[:trim_end], gt_obj.y[:trim_end], 'k-',
                        markevery=markers_on, marker= 'o', color="blue")

        markers_on = [i for i in range(len(gt_obj.x[tirm_start:])) if i%20 == 0]
        line, = ax.plot(gt_obj.x[tirm_start:], gt_obj.y[tirm_start:], 'k-',
                        markevery=markers_on, marker= 'o', color="red")

        final_data = dir + "/data"
        try:
            os.mkdir(final_data)
        except:
            pass
        plt.xlabel('x, [meters]')
        plt.ylabel('y, [meters]')
        plt.savefig(final_data + "/ground_truth_trajectory_matched.png")
        plt.show()
        # plt.plot(gt_obj.x[:trim_end], gt_obj.y[:trim_end])
        # plt.plot(gt_obj.x[tirm_start:], gt_obj.y[tirm_start:])

        # plt.plot(odom_obj.x[:trim_end], odom_obj.y[:trim_end])
        # plt.plot(odom_obj.x[tirm_start:], odom_obj.y[tirm_start:])
    else:
        trim_end = 290
        tirm_start = 320

        fig, ax = plt.subplots(1, 1)
        line, = ax.plot(odom_obj.x, odom_obj.y, 'k-')
        add_arrow_to_line2D(ax, line, arrow_locs=np.linspace(0., 1., 50),
                            arrowstyle='->')

        markers_on = [i for i in range(len(gt_obj.x[:trim_end])) if i%20 == 0]
        line, = ax.plot(gt_obj.x[:trim_end], gt_obj.y[:trim_end], 'k-',
                        markevery=markers_on, marker= 'o', color="blue")

        markers_on = [i for i in range(len(gt_obj.x[tirm_start:])) if i%20 == 0]
        line, = ax.plot(gt_obj.x[tirm_start:], gt_obj.y[tirm_start:], 'k-',
                        markevery=markers_on, marker= 'o', color="red")
        final_data = dir + "/data"
        try:
            os.mkdir(final_data)
        except:
            pass
        plt.xlabel('x, [meters]')
        plt.ylabel('y, [meters]')
        plt.savefig(final_data + "/ground_truth_trajectory.png")
        plt.show()



def plot_errors(odom_object, ground_truth_object, purge=False):

    if purge:
        trim_end = 290
        tirm_start = 290
        void = 100
        # intervals = 10
        
        errors = []
        for i in range(len(odom_object.x)):
            error = math.sqrt((odom_object.x[i] - ground_truth_object.x[i])**2 + (odom_object.y[i] - ground_truth_object.y[i])**2)
            errors.append(error)
        print(len(errors))

        plt.plot(range(0,290),errors[:trim_end])
        plt.plot(range(290,290 + void),[i*0 for i in range(void)], color="white")
        plt.plot(range(290 + void,void+ len(errors)), errors[tirm_start:])

        # x = np.linspace(0., (len(errors) + void)/14.5, intervals)
        plt.xticks([])
        plt.xlabel('time, [seconds]', labelpad=20)
        plt.ylabel('translition error, [meters]')
        final_data = dir + "/data"
        try:
            os.mkdir(final_data)
        except:
            pass
        plt.savefig(final_data + "/translation_error.png")
        plt.show()

        try:
            df = pd.read_csv(final_data + '/results.csv')
        except:
            print("no result.csv file found!")
            
        df['mean_translation _error'] = np.mean(errors)
        df.to_csv(final_data + '/results.csv')

    else:
        errors = []
        for i in range(len(odom_object.x)):
            error = math.sqrt((odom_object.x[i] - ground_truth_object.x[i])**2 + (odom_object.y[i] - ground_truth_object.y[i])**2)
            errors.append(error)
        plt.xlabel('time, [seconds]')
        plt.ylabel('translition error, [meters]')
        plt.plot(errors)
        plt.show()

    # errors = []
    # for i in range(len(odom_object.x)):
    #     error = odom_object.z_1[i] - ground_truth_object.z_1[i]
    #     errors.append(error)

    # plt.plot(errors)
    # plt.show()







odom_object = Odom_points(df=df_odom)
ground_truth_object = GT_points(df=df_gt)

shift_x = ground_truth_object.x[0] - odom_object.x[0]
shift_y = ground_truth_object.y[0] - odom_object.x[0]

odom_object.scale_shift_rotate(scale=1, shift_x=shift_x,shift_y=shift_y,rotate=-6)
# plot_all(odom_obj=odom_object,gt_obj=ground_truth_object)

odom_object.match_counter_points(ground_truth_object)
# odom_object.caclulate_rmse(ground_truth_object)

# plot_all(odom_obj=odom_object,gt_obj=ground_truth_object, match=True)
plot_errors(odom_object=odom_object, ground_truth_object=ground_truth_object, purge=True)

