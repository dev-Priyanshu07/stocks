import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Parameters
window = 20
num_points = 100

# Simulate initial data
np.random.seed(42)
price_data = np.random.normal(loc=100, scale=5, size=num_points)
time_stamps = pd.date_range(start="2023-01-01", periods=num_points, freq="S")

# Create DataFrame
df = pd.DataFrame(data={'Price': price_data}, index=time_stamps)

# Function to calculate Bollinger Bands
def calculate_bollinger_bands(data, window):
    rolling_mean = data['Price'].rolling(window=window).mean()
    rolling_std = data['Price'].rolling(window=window).std()
    data['Middle Band'] = rolling_mean
    data['Upper Band'] = rolling_mean + (rolling_std * 2)
    data['Lower Band'] = rolling_mean - (rolling_std * 2)
    return data

# Initial calculation
df = calculate_bollinger_bands(df, window)

# Plotting setup
fig, ax = plt.subplots()
line_price, = ax.plot(df.index, df['Price'], label='Price')
line_middle, = ax.plot(df.index, df['Middle Band'], label='Middle Band')
line_upper, = ax.plot(df.index, df['Upper Band'], label='Upper Band')
line_lower, = ax.plot(df.index, df['Lower Band'], label='Lower Band')
ax.legend(loc='upper left')

# Function to update the data
def update_data():
    global df
    new_price = np.random.normal(loc=df['Price'].iloc[-1], scale=2)
    new_time = df.index[-1] + pd.Timedelta(seconds=1)
    new_row = pd.DataFrame(data={'Price': [new_price]}, index=[new_time])
    df = pd.concat([df, new_row])
    df = calculate_bollinger_bands(df, window)
    df = df.tail(num_points)

# Function to update the plot
def update_plot(frame):
    update_data()
    line_price.set_data(df.index, df['Price'])
    line_middle.set_data(df.index, df['Middle Band'])
    line_upper.set_data(df.index, df['Upper Band'])
    line_lower.set_data(df.index, df['Lower Band'])
    ax.relim()
    ax.autoscale_view()
    return line_price, line_middle, line_upper, line_lower

# Animation
ani = FuncAnimation(fig, update_plot, interval=1000)

plt.show()
