
import os
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

# fig = plt.gcf()
# fig.set_size_inches(12, 12)
matplotlib.rc('font', **font)


dir = "/home/ali/bagfiles (copy)/"
directories = ["LIO_final", "A-LOAM_final", "FAST_LIO_final", "FAST_LIO_SLAM(SC)_final", 
"F-LOAM_final", "LEGO_LOAM_final", "LINS_final", "LVI_final", "sc-lego-loam_final",
 "orb_slam_2_final", "VINS_final"]

val = []
names = []
d = {}
for item in directories:
    df = pd.read_csv(dir + item + "/data/results.csv")
    d[df['cpu_mean'][0]] = item.replace("_final", "").replace("_", "-").upper()
    val.append(df['cpu_mean'][0])
    names.append(item.replace("_final", "").replace("_", "-").upper())
    print(item.replace("_final", "").upper(), df['cpu_mean'][0])

lists = sorted(d.items()) # sorted by key, return a list of tuples
lists.reverse()
x, y = zip(*lists) # unpack a list of pairs into two tuples


print(x[0], y[0])

fig, ax = plt.subplots()

for i, txt in enumerate(x):
    ax.annotate(round(x[i], 2), (y[i], x[i]), xytext=(i+0.5, x[i]+4.0),
        bbox=dict(boxstyle="round", alpha=1.5), 
        arrowprops = dict(arrowstyle="simple"), fontsize='large')





fig = plt.gcf()
fig.set_size_inches(12, 12)


plt.xlabel('method')
plt.ylabel('CPU usage, [percentage]')
plt.plot(y, x, marker= 'o', color="blue")
plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
fig.savefig("cpu_usage.png", format='png', dpi=600)
plt.show()




# \begin{table}[ht]
# \caption{RMSE comparison of SLAM methods in mine environment.\label{tab:table1}}
# \centering
# \begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|}
# \hline
# Method & LIO & A-LOAM & FAST_LIO & FAST_LIO_SLAM(SC) & F-LOAM & LEGO_LOAM & LINS & LVI & SC-LEGO-LOAM & ORB_SLAM_2 & VINS\\
# \hline
# RMSE & 0.04367 & 0.80067 & 0.02336 & 0.10439 & 1.4916 & 0.4031 & 1.0257 & 0.0177 & 0.5485 & 1.7159 & 4.4368\\
# \hline
# \end{tabular}
# \end{table}