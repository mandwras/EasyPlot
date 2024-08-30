import pandas as pd
import matplotlib.pyplot as plt

# Acceptable temperature ranges
lower_bound = 18.0
upper_bound = 22.0

# Data source path
file_path = 'DummyData.txt'

# Attempt to read the file with a different encoding
try:
    df = pd.read_csv(file_path, encoding='latin1')  # or 'ISO-8859-1', 'cp1252'
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()
except pd.errors.EmptyDataError:
    print("Error: The file is empty.")
    exit()
except pd.errors.ParserError:
    print("Error: The file could not be parsed.")
    exit()
except UnicodeDecodeError as e:
    print(f"Error decoding file: {e}")
    exit()

# Print the first few rows of the DataFrame
print(df.head())
print(df.info())

# Convert 'Celsius(°C)' to numeric values, ignoring errors
df['Celsius(C)'] = pd.to_numeric(df['Celsius(C)'], errors='coerce')

# Convert 'Time' column to datetime
df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

# Check for missing or NaN values
print(df.isna().sum())

# Drop rows with NaN values (optional, if necessary)
df = df.dropna()

# Check if the temperature is within the acceptable range
df['Within Range'] = df['Celsius(C)'].between(lower_bound, upper_bound)

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(df['Time'], df['Celsius(C)'], label='Temperature', marker='o')

# Highlighting the acceptable temperature range
plt.fill_between(df['Time'], lower_bound, upper_bound, color='green', alpha=0.1, label='Acceptable Range')

# Marking points within the acceptable range
plt.scatter(df['Time'][df['Within Range']], df['Celsius(C)'][df['Within Range']], color='green', label='Within Range')

# Marking points outside the acceptable range
plt.scatter(df['Time'][~df['Within Range']], df['Celsius(C)'][~df['Within Range']], color='red', label='Outside Range')

# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Readings vs. Time')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot
plt.show()
