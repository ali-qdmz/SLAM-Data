import os
import pandas as pd

directory = "/home/ali/catkin_ws/src/MULLS/demo_data/pcd"

files = os.listdir(directory)
sorted_names = []
for item in files:
    sorted_names.append(item.replace(".pcd", ""))
sorted_names.sort()

file_counter = 0
main_string = "000000"
for item in sorted_names:
    renamer = str(file_counter)
    os.rename(directory + "/" + item + ".pcd", main_string[:len(main_string) - len(renamer)] + renamer + ".pcd")
    file_counter += 1
    print(file_counter)

print(max(sorted_names))