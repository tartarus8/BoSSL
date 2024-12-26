import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('flight_to_mun_data.csv')

plt.figure(figsize=(10, 5))
plt.plot(data['Time (s)'], data['Velocity (m/s)'], label='Velocity')
plt.title('Velocity vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(data['Time (s)'], data['Mass (kg)'], label='Mass', color='orange')
plt.title('Mass vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Mass (kg)')
plt.grid(True)
plt.legend()
plt.show()