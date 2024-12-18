
import os
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

dir = "/home/ali/bagfiles (copy)/"
directories = ["LIO_final", "A-LOAM_final", "FAST_LIO_final", "FAST_LIO_SLAM(SC)_final", 
"F-LOAM_final", "LEGO_LOAM_final", "LINS_final", "LVI_final", "sc-lego-loam_final",
 "orb_slam_final", "VINS_final"]


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 13}

# fig = plt.gcf()
# fig.set_size_inches(12, 12)
matplotlib.rc('font', **font)


val = []
names = []
d = {}
for item in directories:
    df = pd.read_csv(dir + item + "/data/results.csv")
    d[df['rmse'][0]] = item.replace("_final", "").replace("_", "-").upper()
    val.append(df['rmse'][0])
    names.append(item.replace("_final", "").replace("_", "-").upper())
#     print(item.replace("_final", "").upper(), df['rmse'][0])

lists = sorted(d.items()) # sorted by key, return a list of tuples
lists.reverse()
x, y = zip(*lists) # unpack a list of pairs into two tuples


# print(x[0], y[0])

fig, ax = plt.subplots()

for i, txt in enumerate(x):
        print(txt)
        if round(txt, 2) == 1.86:
                ax.annotate(str(round(x[i], 4)) + "*", (y[i], x[i]), xytext=(i+0.5, x[i]+0.3),
                        bbox=dict(boxstyle="round", alpha=0.1), 
                        arrowprops = dict(arrowstyle="simple"), fontsize='large')
        else:
                ax.annotate(round(x[i], 4), (y[i], x[i]), xytext=(i+0.5, x[i]+0.3),
                        bbox=dict(boxstyle="round", alpha=0.1), 
                        arrowprops = dict(arrowstyle="simple"), fontsize='large')     

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 13.5}

fig = plt.gcf()
fig.set_size_inches(14, 11)
matplotlib.rc('font', **font)

plt.xlabel('method', fontsize='large')
plt.ylabel('root mean square errors, [meters]', fontsize='large')
plt.plot(y, x, marker= 'o', color="blue")
plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='medium')
fig.savefig("rmse.png", format='png', dpi=600)
plt.show()




