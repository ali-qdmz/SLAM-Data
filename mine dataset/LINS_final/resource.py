import random
from time import time
import pandas as pd
import os
import math
from sklearn.metrics import mean_squared_error 
import matplotlib.pyplot as plt
import os

directory_myself = "/home/ali/bagfiles (copy)/LINS_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_image_projection_node_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lidar_mapping_node_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lins_fusion_node_slash_cpu.csv')
# df_cpu_4 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lio_sam_mapOptmization_slash_cpu.csv')


df_mem_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_image_projection_node_slash_mem.csv')
df_mem_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lidar_mapping_node_slash_mem.csv')
df_mem_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lins_fusion_node_slash_mem.csv')

df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3 

df_cpu_total.plot()
plt.xlabel('Seconds')
plt.ylabel('Percent')
plt.savefig(directory_myself + '/data/cpu_usage.png')
plt.show()


df_mem_total = df_mem_1['data'] + df_mem_2['data'] + df_mem_3['data']
df_mem_total.plot()
plt.xlabel('Seconds')
plt.ylabel('bits')
plt.savefig(directory_myself + '/data/mem_usage.png')
plt.show()

print(df_cpu_total.mean(), df_mem_total.mean())