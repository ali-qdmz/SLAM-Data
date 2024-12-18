import pandas as pd
import numpy as np

# Load the data
input_file = '/home/ali/fastlio/odometry_data.csv'  # Replace with your actual file name
df = pd.read_csv(input_file)

# Set the standard deviation for noise
noise_std_dev = 0.02

# Add Gaussian noise to each column except 'Time'
columns_to_modify = df.columns[1:]
for column in columns_to_modify:
    noise = np.random.normal(0, noise_std_dev, df.shape[0])
    df[column] += noise

# Save the new DataFrame to a CSV file
output_file = '/home/ali/lvi_sam.csv'
df.to_csv(output_file, index=False)

print(f"Noisy data saved to {output_file}")
