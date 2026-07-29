import asyncio
import json
import websockets
import threading
from websocket import WebSocketApp
from __functions import kalsh_header_for_wss

kalshi_key_id = 'your_key_here'
wss_header = kalsh_header_for_wss(kalshi_key_id)

poly_ws_url = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
kalsh_ws_url = "wss://external-api-ws.kalshi.com/trade-api/ws/v2"
port_url = "https://api.elections.kalshi.com/trade-api/v2/portfolio/orders"

poly_clob_token_id = "copy_and_paste_here"
kalsh_market_ticker = "copy_and_paste_here"

poly_price = None
kalshi_ask = None

async def kalshi_ws():
    global kalshi_ask
    async with websockets.connect(kalsh_ws_url, additional_headers=wss_header) as ws:
        sub = {"id": 1, "cmd": "subscribe", "params": {"channels": ["ticker"], "market_ticker": kalsh_market_ticker}}
        await ws.send(json.dumps(sub))
        async for msg in ws:
            data = json.loads(msg)
            if data.get("type") == "ticker":
                yes_ask_dollars = data["msg"]["yes_ask_dollars"]
                kalshi_ask = int(round(float(yes_ask_dollars) * 100))

def polymarket_ws(url, token_id):
    global poly_price
    def on_message(ws, message):
        global poly_price
        data = json.loads(message)
        if data.get("event_type") == "price_change":
            for change in data["price_changes"]:
                if change["asset_id"] == token_id:
                    poly_price = int(float(change['best_ask']) * 100)
    def on_open(ws):
        ws.send(json.dumps({"assets_ids": [token_id], "type": "market"}))
    ws = WebSocketApp(url, on_message=on_message, on_open=on_open)
    ws.run_forever()

async def compare_loop():
    done = False
    while True:
        if poly_price and kalshi_ask:
            diff = (poly_price + kalshi_ask) - 100
            print(f"Poly: {poly_price} | Kal: {kalshi_ask} | Diff: {diff}")
            if diff < 0:
                print('buy')
        await asyncio.sleep(0)

async def main():
    threading.Thread(target=polymarket_ws, args=(poly_ws_url, poly_clob_token_id), daemon=True).start()
    await asyncio.gather(kalshi_ws(), compare_loop())

asyncio.run(main())
