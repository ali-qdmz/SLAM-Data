import random
from time import time
import pandas as pd
import os
import math
from sklearn.metrics import mean_squared_error 
import matplotlib.pyplot as plt
import os

directory_myself = "/home/ali/bagfiles (copy)/F-LOAM_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_base_link_slash_trajectory_server_loam_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_floam_laser_mapping_node_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_floam_laser_processing_node_slash_cpu.csv')
df_cpu_4 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_floam_odom_estimation_node_slash_cpu.csv')
df_cpu_5 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_velodyne_nodelet_manager_cloud_slash_cpu.csv')
df_cpu_6 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_velodyne_nodelet_manager_driver_slash_cpu.csv')
df_cpu_7 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_velodyne_nodelet_manager_laserscan_slash_cpu.csv')
df_cpu_8 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_velodyne_nodelet_manager_slash_cpu.csv')
df_cpu_9 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_word2map_tf_slash_cpu.csv')



df_mem_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_base_link_slash_trajectory_server_loam_slash_mem.csv')
df_mem_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_floam_laser_mapping_node_slash_mem.csv')
df_mem_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_floam_laser_processing_node_slash_mem.csv')
df_mem_4 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_floam_odom_estimation_node_slash_mem.csv')
df_mem_5 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_velodyne_nodelet_manager_cloud_slash_mem.csv')
df_mem_6 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_velodyne_nodelet_manager_driver_slash_mem.csv')
df_mem_7 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_velodyne_nodelet_manager_laserscan_slash_mem.csv')
df_mem_8 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_velodyne_nodelet_manager_slash_mem.csv')
df_mem_9 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_word2map_tf_slash_mem.csv')


df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3  + df_cpu_4['data']/3  + df_cpu_5['data']/3  + df_cpu_6['data']/3  + df_cpu_7['data']/3  + df_cpu_8['data']/3  + df_cpu_9['data']/3

df_cpu_total = df_cpu_total.iloc[0:len(df_cpu_total):1]
ax = df_cpu_total.plot()
ax.set_xlim(0, len(df_cpu_total))

plt.xlabel('time, [seconds]')
plt.ylabel('usage, [percent]')
plt.savefig(directory_myself + '/data/cpu_usage.png')
plt.show()

df_mem_total = df_mem_1['data'] + df_mem_2['data'] + df_mem_3['data'] + df_mem_4['data'] + df_mem_5['data'] + df_mem_6['data'] + df_mem_7['data'] + df_mem_8['data'] + df_mem_9['data']

df_mem_total = df_mem_total.iloc[0:len(df_mem_total):2]
print(len(df_mem_total))
ax = df_mem_total.plot()
ax.set_xlim(0, len(df_mem_total))

df_mem_total.plot()
plt.xlabel('time, [seconds]')
plt.ylabel('usage, [bits]')
plt.savefig(directory_myself + '/data/mem_usage.png')
plt.show()

print(df_cpu_total.mean(), df_mem_total.mean())