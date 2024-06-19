import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the dataset
df = pd.read_csv(r"C:\Users\seiff\Desktop\Python in data\Weather data analysis\weather_data.csv")

# Convert Date_Time to datetime format
df['Date_Time'] = pd.to_datetime(df['Date_Time'])

# Calculate average temperature for each location
avg_temp = df.groupby('Location')['Temperature_C'].mean().reset_index()

# Plotting the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='Location', y='Temperature_C', data=avg_temp,
            edgecolor='black')  # Adding edgecolor for better separation
plt.title('Average Temperature in Each Location')
plt.xlabel('Location')
plt.ylabel('Average Temperature (Celsius)')
plt.xticks(rotation=45)

# Adding labels with average temperature values
for index, row in avg_temp.iterrows():
    plt.text(index, row['Temperature_C'] + 0.2, round(row['Temperature_C'], 2), 
             color='black', ha='center')

plt.tight_layout()
plt.show()

# Pheonix has a significantly lower tempreature average than all the other states, let's investigate why
# I will get the months

df['Month'] = df['Date_Time'].dt.month

# Group by location then month to get the average tempreature for each state per month
average_month_temp = df.groupby(['Location', 'Month'])['Temperature_C'].mean().reset_index()

# Let's plot this data
plt.figure(figsize=(12, 8))
sns.lineplot(x='Month', y='Temperature_C', hue='Location', data=average_month_temp, marker='o')
plt.title('Average Monthly Temperature Trends (Different Cities)')
plt.xlabel('Month')
plt.ylabel('Average Temperature (Celsius)')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(loc='upper right')
plt.show()

# As it turns out the reason why this happens is that Phoenix has significantly lower tempreature in January and Feburay while in all the other states temperature is stable.

# I want to see if pheonix experiences both high and low temps or just low temps compared to other states

# I will create a table for max temp and another for min temp for each state and join those to compare.
max_temp = df.groupby('Location')['Temperature_C'].max().reset_index()
min_temp = df.groupby('Location')['Temperature_C'].min().reset_index()

# Merge max and min temperatures into one DataFrame
temp_summary = pd.merge(max_temp, min_temp, on='Location', suffixes=('_max', '_min'))

# Create a table with custom cell colors
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis('off')  # Turn off axis for table display
ax.set_title('Max and Min Temperatures in Each Location')

# Prepare table data
table_data = []
for i, row in temp_summary.iterrows():
    table_data.append([row['Location'], row['Temperature_C_max'], row['Temperature_C_min']])

# Add colors to the table
ax.table(cellText=table_data, colLabels=['Location', 'Max Temp (C)', 'Min Temp (C)'], loc='center')

plt.show()
