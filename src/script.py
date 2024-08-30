import pandas as pd
import matplotlib.pyplot as plt


#acceptable temp ranges
lower_bound = 18.0
upper_bound = 22.0

#data src
file_path = 'DummyData.txt'
df = pd.read_csv(file_path)

#conversions
df['Celsius(°C)'] = pd.to_numeric(df['Celsius(°C)'], errors='coerce')

#temp check
df['Within Range'] = df['Celsius(°C)'].between(lower_bound, upper_bound)

#data plot
plt.figure(figsize=(10, 6))
plt.plot(df['Time'], df['Celsius(°C)'], label='Temperature', marker='o')

#highlight
plt.fill_between(df['Time'], lower_bound, upper_bound, color='green', alpha=0.1, label='Acceptable Range')
plt.scatter(df['Time'][df['Within Range']], df['Celsius(°C)'][df['Within Range']], color='green', label='Within Range')
plt.scatter(df['Time'][~df['Within Range']], df['Celsius(°C)'][~df['Within Range']], color='red', label='Outside Range')

#labels
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Readings vs. Time')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()