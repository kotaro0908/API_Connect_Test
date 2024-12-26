import websocket
import json

def on_open(ws):
    print("さすが！接続完了しました。Tickerを購読します。")
    subscribe_msg = {
        "command": "subscribe",
        "channel": "ticker",
        "symbol": "BTC_JPY"
    }
    ws.send(json.dumps(subscribe_msg))

def on_message(ws, message):
    data = json.loads(message)
    print("受信:", data)

def on_error(ws, error):
    print("エラーが発生しました:", error)

def on_close(ws, close_status_code, close_msg):
    print("接続が閉じられました。ステータスコード:", close_status_code, "メッセージ:", close_msg)

if __name__ == "__main__":
    # WebSocket接続のトレースログを有効にしたい場合はコメントアウトを外す
    # websocket.enableTrace(True)

    ws = websocket.WebSocketApp(
        "wss://api.coin.z.com/ws/public/v1",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
