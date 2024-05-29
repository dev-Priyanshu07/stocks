import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
import random
import time

def calculate_supertrend(df, period=7, atr_multiplier=3):
    hl2 = (df['High'] + df['Low']) / 2
    atr = df['Close'].rolling(window=period).apply(lambda x: np.mean(np.abs(np.diff(x))), raw=False)
    df['ATR'] = atr

    df['UpperBand'] = hl2 + (atr_multiplier * df['ATR'])
    df['LowerBand'] = hl2 - (atr_multiplier * df['ATR'])

    df['Supertrend'] = np.nan

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['Close'].iloc[current] > df['UpperBand'].iloc[previous]:
            df['Supertrend'].iloc[current] = df['LowerBand'].iloc[current]
        elif df['Close'].iloc[current] < df['LowerBand'].iloc[previous]:
            df['Supertrend'].iloc[current] = df['UpperBand'].iloc[current]
        else:
            df['Supertrend'].iloc[current] = df['Supertrend'].iloc[previous]
            if df['Supertrend'].iloc[current] > df['UpperBand'].iloc[current]:
                df['Supertrend'].iloc[current] = df['UpperBand'].iloc[current]
            elif df['Supertrend'].iloc[current] < df['LowerBand'].iloc[current]:
                df['Supertrend'].iloc[current] = df['LowerBand'].iloc[current]

    return df

def data_simulator():
    data = []
    initial_price = 100
    for _ in range(10):  # Reduced for quicker testing
        close_price = initial_price + random.uniform(-1, 1)
        high_price = close_price + random.uniform(0, 0.5)
        low_price = close_price - random.uniform(0, 0.5)
        data.append({'High': high_price, 'Low': low_price, 'Close': close_price})
        initial_price = close_price
        time.sleep(0.1)  # Simulate delay for generating new data
    return pd.DataFrame(data)

def update_supertrend(frame, df, ax1, line1, line2):
    # Get new data from the simulator
    new_data = data_simulator()
    df = pd.concat([df, new_data], ignore_index=True)

    # Calculate Supertrend
    df = calculate_supertrend(df)

    # Debug: Print the latest data
    print(df.tail())

    # Clear and plot new data
    ax1.clear()
    ax1.plot(df.index, df['Close'], label='Close Price', color='blue')
    ax1.plot(df.index, df['Supertrend'], label='Supertrend', color='red')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price')
    ax1.legend()

    # Update lines
    line1.set_data(df.index, df['Close'])
    line2.set_data(df.index, df['Supertrend'])

    return line1, line2

if __name__ == "__main__":
    df = data_simulator()
    df = calculate_supertrend(df)

    fig, ax1 = plt.subplots()
    line1, = ax1.plot(df.index, df['Close'], label='Close Price', color='blue')
    line2, = ax1.plot(df.index, df['Supertrend'], label='Supertrend', color='red')

    ani = animation.FuncAnimation(fig, update_supertrend, fargs=(df, ax1, line1, line2), interval=1000, cache_frame_data=False)

    plt.show()
