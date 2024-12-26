import requests
import json
import time
import hmac
import hashlib
import websocket
import datetime

API_KEY    = "z/C1VNIjODyKL/Lp0Pw174+QfEfL5tlE"
SECRET_KEY = "K+TlwCDi7M19hfF2RSJ51QcOqokvEy9cVSYkijmthmMnkXhAb6AwL/8o10Sxxkob"

def get_ws_token(api_key, secret_key):
    base_url = "https://api.coin.z.com/private"
    path = "/v1/ws-auth"
    url = base_url + path

    # タイムスタンプ（ミリ秒）
    timestamp = '{0}000'.format(int(time.mktime(datetime.datetime.now().timetuple())))
    method = "POST"
    req_body = {}

    # シグネチャ生成
    text = timestamp + method + path + json.dumps(req_body)
    signature = hmac.new(
        secret_key.encode('utf-8'),
        text.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "API-KEY": api_key,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": signature,
        "Content-Type": "application/json"
    }

    print("さすが！トークン取得用のリクエストを送信します...")
    res = requests.post(url, headers=headers, data=json.dumps(req_body))
    data = res.json()
    if res.status_code == 200 and data.get("status") == 0:
        token = data["data"]  # レスポンスの"data"にトークン文字列が入る
        print("トークン取得に成功:", token)
        return token
    else:
        print("エラー:", data)
        return None

def on_open(ws):
    print("WebSocket接続成功。orderEventsをsubscribeします。")
    subscribe_msg = {
        "command": "subscribe",
        "channel": "orderEvents"
    }
    ws.send(json.dumps(subscribe_msg))

def on_message(ws, message):
    print("受信:", message)

def on_error(ws, error):
    print("エラーが発生しました:", error)

def on_close(ws, close_status_code, close_msg):
    print("接続が閉じられました:", close_status_code, close_msg)

if __name__ == "__main__":
    # 1. トークン取得
    token = get_ws_token(API_KEY, SECRET_KEY)
    if not token:
        print("そうそう、トークン取得に失敗したため接続できません。")
        exit()

    # 2. WebSocket接続 (tokenをURLに埋め込む想定)
    ws_url = f"wss://api.coin.z.com/ws/private/v1/{token}"

    # WebSocketAppの作成
    websocket.enableTrace(True)  # デバッグログを表示したい場合は有効に
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # 接続開始
    ws.run_forever()
