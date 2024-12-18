import random
from time import time
import pandas as pd
import os
import math
from sklearn.metrics import mean_squared_error 
import matplotlib.pyplot as plt
import os

directory_myself = "/home/ali/bagfiles (copy)/orb_slam_2_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_orb_slam2_mono_slash_cpu.csv')

df_mem_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_orb_slam2_mono_slash_mem.csv')

df_cpu_total = df_cpu_1['data']/3

df_cpu_total = df_cpu_total.iloc[0:len(df_cpu_total):1]
ax = df_cpu_total.plot()
ax.set_xlim(0, len(df_cpu_total))

plt.xlabel('time, [seconds]')
plt.ylabel('usage, [percent]')
plt.savefig(directory_myself + '/data/cpu_usage.png')
plt.show()

df_mem_total = df_mem_1['data']

df_mem_total = df_mem_total.iloc[0:len(df_mem_total):1]
print(len(df_mem_total))
ax = df_mem_total.plot()
ax.set_xlim(0, len(df_mem_total))

df_mem_total.plot()
plt.xlabel('time, [seconds]')
plt.ylabel('usage, [bits]')
plt.savefig(directory_myself + '/data/mem_usage.png')
plt.show()

print(df_cpu_total.mean(), df_mem_total.mean())