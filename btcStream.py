import pandas as pd
import websocket
import json
import dateutil.parser
import datetime
from datetime import date, datetime, timedelta

socket = "wss://ws-feed.exchange.coinbase.com"

minutes_processed = {}
minute_candlesticks = []
current_tick = None
prevoius_tick = None

def onOpen(ws):
    print("Connection established")
    subscribe_msg = {
        "type": "subscribe",
        "channels": [
            "level2",
            "heartbeat",
            {
                "name": "ticker",
                "product_ids": [
                    "BTC-USD"
                ]
            }
        ]
    }

    ws.send(json.dumps(subscribe_msg)) #Converting the subscribe_msg dictionary to a json string


def on_msg(ws, msg):
    global current_tick, prevoius_tick # These are now accessible by the function
    prevoius_tick = current_tick
    current_tick = json.loads(msg)

    # print(current_tick)

    print("***Received tick***")
    print("Price : {} | Time : {}".format(current_tick['price'], current_tick['time']))

    tick_datetime_object = dateutil.parser.parse(current_tick['time']) # datetime object
    timenow = tick_datetime_object + timedelta(hours=5.5)
    tick_dt = timenow.strftime("%m/%d/%Y %H:%M")

    

    print(tick_datetime_object.minute)
    print(tick_dt)

    # if tick_dt not in minutes_processed:
    #     print("New Candlestick")

    #     if len(minute_candlesticks) > 0:
    #         minute_candlesticks[-1]['close'] = prevoius_tick['price']

    #     minute_candlesticks.append(
    #         {
    #             'minute' : tick_dt,
    #             'open' :  current_tick['price'],
    #             'high' : current_tick['price'],
    #             'low' : current_tick['price']
    #         }
    #     )    

    #     df = pd.DataFrame(minute_candlesticks[:-1])
    #     df.to_csv("btcStream.csv")
    #     minutes_processed[tick_dt] = True


    if tick_dt not in minutes_processed:
        print("New Candlestick")

        if len(minute_candlesticks) > 0:
            minute_candlesticks[-1]['close'] = prevoius_tick['price']

        minute_candlesticks.append(
            {
                'minute' : tick_dt,
                'open' :  current_tick['price'],
                'high' : current_tick['price'],
                'low' : current_tick['price']
            }
        )    

        df = pd.DataFrame(minute_candlesticks[:-1])
        df.to_csv("btcStream.csv")
        minutes_processed[tick_dt] = True


    if len(minute_candlesticks) > 0:
        considered_candlestick =  minute_candlesticks[-1]
 
        if current_tick['price'] > considered_candlestick['high']:
            considered_candlestick['high'] = current_tick['price']
        if current_tick['price'] < considered_candlestick['low']:
            considered_candlestick['low'] = current_tick['price']

        print("***CandleStick***")
        for x in minute_candlesticks:
            print(x)


ws = websocket.WebSocketApp(socket, on_open= onOpen, on_message= on_msg)
ws.run_forever()