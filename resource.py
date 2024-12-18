import random
from time import time
import pandas as pd
import os
import math
from sklearn.metrics import mean_squared_error 
import matplotlib.pyplot as plt
import os

directory_myself = "/home/ali/bagfiles (copy)/LVI_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_featureExtraction_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_imageProjection_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_imuPreintegration_slash_cpu.csv')
df_cpu_4 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_mapOptmization_slash_cpu.csv')
df_cpu_5 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_robot_state_publisher_slash_cpu.csv')



df_mem_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_featureExtraction_slash_mem.csv')
df_mem_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_imageProjection_slash_mem.csv')
df_mem_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_imuPreintegration_slash_mem.csv')
df_mem_4 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_mapOptmization_slash_mem.csv')
df_mem_5 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_robot_state_publisher_slash_mem.csv')
print(len(df_cpu_1), len(df_cpu_2), len(df_cpu_3), len(df_cpu_4), len(df_cpu_5))
df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3  + df_cpu_4['data']/3  + df_cpu_5['data']/3 

df_cpu_total = df_cpu_total.iloc[0:700:4]
ax = df_cpu_total.plot()
ax.set_xlim(0, len(df_cpu_total))

plt.xlabel('Seconds')
plt.ylabel('Percent')
plt.savefig(directory_myself + '/data/cpu_usage.png')
plt.show()

df_mem_total = df_mem_1['data'] + df_mem_2['data'] + df_mem_3['data'] + df_mem_4['data'] + df_mem_5['data']

df_mem_total = df_mem_total.iloc[0:700:4]
print(len(df_mem_total))
ax = df_mem_total.plot()
ax.set_xlim(0, len(df_mem_total))

df_mem_total.plot()
plt.xlabel('Seconds')
plt.ylabel('bits')
plt.savefig(directory_myself + '/data/mem_usage.png')
plt.show()

print(df_cpu_total.mean(), df_mem_total.mean())