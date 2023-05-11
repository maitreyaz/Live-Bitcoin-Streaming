import pandas as pd
import datetime
from datetime import date, datetime
import matplotlib.animation as animation
import mplfinance as mplf

fig = mplf.figure(style = 'charles', figsize = (7, 8))
ax1 = fig.add_subplot(1, 1, 1)

def animate(ival):
    df = pd.read_csv('btcStream.csv', index_col=0)
    df['minute'] = pd.to_datetime(df['minute'], format="%m/%d/%Y %H:%M")
    df.set_index('minute', inplace=True)

    

    ax1.clear
    mplf.plot(df, ax=ax1, type= 'candle', ylabel = 'Price (US$)')

ani = animation.FuncAnimation(fig, animate, interval=250)    

mplf.show()