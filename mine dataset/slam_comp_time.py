import random
from time import time
import pandas as pd
import os
import math
from sklearn.metrics import mean_squared_error 
import matplotlib.pyplot as plt
import os


print("fk")
directory_myself = "/home/ali/bagfiles (copy)/okvis_odometry"
#directory_myself = "/home/ali/bagfiles (copy)/FLOAM"

def calc_data():
    global directory_myself
    x_gt = "x"
    y_gt = "y"
    z_gt = "z"
    orient_gt = "w"

    x_loc = "x"
    y_loc = "y"
    z_loc = "z"
    orinet_loc = "w"

    
    final_data = directory_myself + "/data"
    try:
        os.mkdir(final_data)
    except:
        pass



    def format_with_commas(n):
        l = list(str(n))
        temp_l = l.copy()
        if (n < 0):
            return('-' + str(format_with_commas(-n)))
        else:
            for i in range(len(temp_l), -1, -1):
                if ((len(temp_l) - i)  == 3):
                    l.insert(i, ',')
                if ((len(temp_l) - i)%3 == 0 and (len(temp_l) - i) > 3):
                    l.insert(i, ',')
            s = ''
            for i in range(len(l)):
                s += l[i]
            return s



    print()
    print()


    while True:
        try:
            dir = directory_myself
            files = [f for f in os.listdir(dir) if f.endswith(".csv")]
            for i in range(len(files)):
                files[i] = files[i].replace("_slash_","/")

            ct = 1
            dic = {}
            for f in files:
                print(ct,": ", f.replace(".csv", ""))
                dic[ct] = f
                ct += 1
            break
        except:
            print("please insert a valid location")

    print()
    print()
    while True:
        try:
            ground_truth = int(input("select the topic related to the ground truth: "))
            localization = int(input("select the topic related to the method localization: "))
            break
        except:
            print("please insert the corresponding number")

    ground_truth = dic[ground_truth]
    localization = dic[localization]

    df_ground_truth = pd.read_csv(dir + "/" + ground_truth.replace("/","_slash_"))
    df_localization = pd.read_csv(dir + "/" + localization.replace("/","_slash_"))

    if len(df_ground_truth) > len(df_localization):
        data = []
        for i in range(len(df_localization)):
            timestamp_loc = df_localization["rosbagTimestamp"][i]
            df_sort = df_ground_truth.iloc[(df_ground_truth['rosbagTimestamp']-timestamp_loc).abs().argsort()[:2]]
            print(df_ground_truth.loc[df_sort.index.tolist()[0]])
            print(df_localization.loc[i])
            print("===============")
            data.append(df_ground_truth.loc[df_sort.index.tolist()[0]])

        temp_df = pd.DataFrame(columns=df_ground_truth.columns, data=data)
        temp_df.to_csv(final_data + "/ground_truth.csv")
        df_localization.to_csv(final_data + "/localization.csv")

    else:
        l = []
        data = []
        for i in range(len(df_ground_truth)):
            timestamp_loc = df_ground_truth["rosbagTimestamp"][i]
            df_sort = df_localization.iloc[(df_localization['rosbagTimestamp']-timestamp_loc).abs().argsort()[:2]]
            nearest_odom = df_localization.loc[df_sort.index.tolist()[0]].rosbagTimestamp
            gt_timestamp = timestamp_loc
            l.append(nearest_odom)
            print(format_with_commas(gt_timestamp), format_with_commas(nearest_odom))
            print("===============")        
            data.append(df_localization.loc[df_sort.index.tolist()[0]])
        print(len(l))
        print(len(set(l)))
        temp_df = pd.DataFrame(columns=df_localization.columns, data=data)
        temp_df.to_csv(final_data + "/localization.csv")
        df_ground_truth.to_csv(final_data + "/ground_truth.csv")


def extract_data():
    global directory_myself
    final_data = directory_myself + "/data"
    try:
        os.mkdir(final_data)
    except:
        pass

    df_gt = pd.read_csv(final_data + "/ground_truth.csv")
    df_odom = pd.read_csv(final_data + "/localization.csv")

    x_odom = df_odom['x']
    y_odom = df_odom['y']
    z_odom = df_odom['z']

    x_gt = df_gt['x'] 
    y_gt = df_gt['y']
    z_gt = df_gt['z']

    plt.plot(x_odom, y_odom)
    plt.plot(x_gt, y_gt)
    plt.xlabel('Meters')
    plt.ylabel('Meters')
    plt.savefig(final_data + "/trajectory.png")
    plt.show()




    ct = min(len(df_gt), len(df_odom))
    realVals = (x_gt.pow(2) + y_gt.pow(2) + z_gt.pow(2))[:ct]
    realVals = realVals.pow(0.5)

    predictedVals = (x_odom.pow(2) + y_odom.pow(2) + z_odom.pow(2))[:ct]
    predictedVals = predictedVals.pow(0.5)
    mse = mean_squared_error(realVals, predictedVals)
    print()
    print()
    print("root mean square equals to: ", mse)


    translation_err_cum = []
    orientation_err_cum = []
    data = []
    for i in range(1 ,ct):
        trans_err = math.sqrt((df_gt['x'][i] - df_odom['x'][i])**2 + 
        (df_gt['y'][i] - df_odom['y'][i])**2 +
        (df_gt['z'][i] - df_odom['z'][i])**2)

        orientation_err = df_gt['w'][i] - df_odom['w'][i]
        data.append([trans_err, orientation_err])

    final_df = pd.DataFrame(columns=["translation_err", "orientation_err"],data=data)
    final_df.to_csv(final_data + "/results.csv")

    final_df["translation_err"].plot()
    plt.xlabel('Timestamps')
    plt.ylabel('Meters')
    plt.savefig(final_data + "/translation_error.png")
    plt.show()

    final_df["orientation_err"].plot()
    plt.xlabel('Timestamps')
    plt.ylabel('Degrees')
    plt.savefig(final_data + "/orientation_error.png")
    plt.show()






    data= []
    try:
        cpu_usage = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_vins_estimator_slash_cpu.csv')
        memory_usage = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_vins_estimator_slash_mem.csv')

        cpu = cpu_usage['data'].plot()
        fig = cpu.get_figure()
        plt.xlabel('Seconds')
        plt.ylabel('Percent')
        plt.savefig(final_data + '/cpu_usage.png')
        cpu_mean = cpu_usage['data'].mean()
        plt.cla()


        memory = memory_usage['data'].plot()
        fig = memory.get_figure()
        plt.xlabel('Seconds')
        plt.ylabel('bits')
        plt.savefig(final_data + '/memory_usage.png')
        memory_mean = memory_usage['data'].mean()
    except Exception as e:
        print(e)
        cpu_mean = 'NA'
        memory_mean = 'NA'
    data.append(mse)
    data.append(cpu_mean)
    data.append(memory_mean)

    algorithm_data = pd.DataFrame(columns=['rmse', 'cpu_mean', 'memory_mean'], data=[data])
    algorithm_data.to_csv(final_data + '/algorithm data.csv')



calc_data()
extract_data()
