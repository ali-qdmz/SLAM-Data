import pandas as pd
import matplotlib.pyplot as plt

dir = "/home/ali/bagfiles (copy)/"

# directories = ["LIO_final", "A-LOAM_final", "FAST_LIO_final", "FAST_LIO_SLAM(SC)_final", 
# "F-LOAM_final", "ISCLOAM_final", "LEGO_LOAM_final", "LINS_final", "LVI_final", "sc-lego-loam_final"]

directories = ["LIO_final", "A-LOAM_final", "FAST_LIO_final", "FAST_LIO_SLAM(SC)_final", 
"F-LOAM_final", "LEGO_LOAM_final", "LINS_final", "LVI_final", "sc-lego-loam_final"]


val = []
names = []
d = {}
for item in directories:
    df = pd.read_csv(dir + item + "/data/results.csv")
    d[df['rmse'][0]] = item.replace("_final", "")
    val.append(df['rmse'][0])
    names.append(item.replace("_final", ""))


lists = sorted(d.items()) # sorted by key, return a list of tuples
lists.reverse()
x, y = zip(*lists) # unpack a list of pairs into two tuples



# plt.xlabel('method')
# plt.ylabel('root mean square errors, [meters]')
# plt.plot(y, x, marker= 'o', color="blue")
# plt.show()


val = []
names = []
d = {}
for item in directories:
    df = pd.read_csv(dir + item + "/data/results.csv")
    val.append(df['rmse'][0])
    names.append(item.replace("_final", ""))



markers_on = [i for i in range(180) if i%3 == 0]
directory_myself = "/home/ali/bagfiles (copy)/A-LOAM_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_alaserMapping_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_alaserOdometry_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_ascanRegistration_slash_cpu.csv')
df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3
df_cpu_total = df_cpu_total.iloc[0:len(df_cpu_total):1]
ax = df_cpu_total.plot(label='A LOAM', markevery=markers_on, marker= '.', color="black")
ax.set_xlim(0, len(df_cpu_total))





directory_myself = "/home/ali/bagfiles (copy)/FAST_LIO_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_laserMapping_slash_cpu.csv')
df_cpu_total = df_cpu_1['data']/3
df_cpu_total = df_cpu_total.iloc[0:len(df_cpu_total):1]
ax = df_cpu_total.plot(label='FAST LIO', markevery=markers_on, marker= 'v', color="black")
ax.set_xlim(0, len(df_cpu_total))






directory_myself = "/home/ali/bagfiles (copy)/FAST_LIO_SLAM(SC)_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_alaserMapping_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_alaserOdometry_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_alaserPGO_slash_cpu.csv')
df_cpu_4 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_ascanRegistration_slash_cpu.csv')
df_cpu_6 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_laserMapping_slash_cpu.csv')
df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3  + df_cpu_4['data']/3  +  df_cpu_6['data']/3 
df_cpu_total = df_cpu_total.iloc[0:len(df_cpu_total):1]
ax = df_cpu_total.plot(label='FAST LIO SC', markevery=markers_on, marker= '1', color="black")
ax.set_xlim(0, len(df_cpu_total))






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
df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3  + df_cpu_4['data']/3  + df_cpu_5['data']/3  + df_cpu_6['data']/3  + df_cpu_7['data']/3  + df_cpu_8['data']/3  + df_cpu_9['data']/3
df_cpu_total = df_cpu_total.iloc[0:len(df_cpu_total):1]
ax = df_cpu_total.plot(label='F LOAM', markevery=markers_on, marker= '2', color="black")
ax.set_xlim(0, len(df_cpu_total))





markers_on = [i for i in range(180) if i%5 == 0]
directory_myself = "/home/ali/bagfiles (copy)/LEGO_LOAM_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_featureAssociation_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_imageProjection_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_mapOptmization_slash_cpu.csv')
df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3
df_cpu_total = df_cpu_total.iloc[0:len(df_cpu_total):1]
ax = df_cpu_total.plot(label='LEGO LOAM', markevery=markers_on, marker= 's', color="black")
ax.set_xlim(0, len(df_cpu_total))







directory_myself = "/home/ali/bagfiles (copy)/LINS_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_image_projection_node_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lidar_mapping_node_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lins_fusion_node_slash_cpu.csv')
df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3 
df_cpu_total.plot(label='LINS', markevery=markers_on, marker= 'P', color="black")






directory_myself = "/home/ali/bagfiles (copy)/LIO_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lio_sam_featureExtraction_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lio_sam_imageProjection_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lio_sam_imuPreintegration_slash_cpu.csv')
df_cpu_4 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lio_sam_mapOptmization_slash_cpu.csv')
df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3  + df_cpu_4['data']/3
df_cpu_total = df_cpu_total.iloc[0:len(df_cpu_total):2]
ax = df_cpu_total.plot(label='LIO', markevery=markers_on, marker= '*', color="black")
ax.set_xlim(0, len(df_cpu_total))


markers_on = [i for i in range(181) if i%15 == 0]
directory_myself = "/home/ali/bagfiles (copy)/LVI_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_featureExtraction_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_imageProjection_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_imuPreintegration_slash_cpu.csv')
df_cpu_4 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_mapOptmization_slash_cpu.csv')
df_cpu_5 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_lvi_sam_robot_state_publisher_slash_cpu.csv')
df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3  + df_cpu_4['data']/3  + df_cpu_5['data']/3 
df_cpu_total = df_cpu_total.iloc[0:700:4]
ax = df_cpu_total.plot(label='LVI', marker= 'x', color="black")
ax.set_xlim(0, len(df_cpu_total))









directory_myself = "/home/ali/bagfiles (copy)/sc-lego-loam_final"
df_cpu_1 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_featureAssociation_slash_cpu.csv')
df_cpu_2 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_imageProjection_slash_cpu.csv')
df_cpu_3 = pd.read_csv(directory_myself + '/_slash_cpu_monitor_slash_mapOptmization_slash_cpu.csv')
df_cpu_total = df_cpu_1['data']/3 + df_cpu_2['data']/3 + df_cpu_3['data']/3
df_cpu_total = df_cpu_total.iloc[0:len(df_cpu_total):1]
ax = df_cpu_total.plot(label='LEGO-LOAM', marker= 'd', color="black")
ax.set_xlim(0, len(df_cpu_total))



plt.xlabel('time, [seconds]')
plt.ylabel('usage, [percent]')
plt.legend(loc="upper right")
plt.show()