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
        token = data["data"]  # レスポンスの"data"がトークン
        print("トークン取得に成功:", token)
        return token
    else:
        print("エラー:", data)
        return None

def connect_ws_with_token(token):
    ws_url = "wss://api.coin.z.com/ws/private/v1"

    def on_open(ws):
        print("WebSocket接続成功。トークンでログインします。")
        # トークンを使ったログインコマンドを送信
        login_msg = {
            "command": "login",
            "token": token
        }
        ws.send(json.dumps(login_msg))

    def on_message(ws, message):
        data = json.loads(message)
        print("受信:", data)
        # ここで "status":0 が返ってくれば認証OKです

    def on_error(ws, error):
        print("エラーが発生しました:", error)

    def on_close(ws, close_status_code, close_msg):
        print("接続が閉じられました:", close_status_code, close_msg)

    # WebSocketAppの定義
    ws_app = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    # イベントループ開始
    ws_app.run_forever()

if __name__ == "__main__":
    # 1. トークン取得
    token = get_ws_token(API_KEY, SECRET_KEY)
    # 2. トークンが取れたらWebSocketに接続してログイン
    if token:
        connect_ws_with_token(token)
    else:
        print("そうそう、トークン取得に失敗したため接続できません。")


#
# import requests
# import json
# import hmac
# import hashlib
# import time
# from datetime import datetime
#
# apiKey    = 'z/C1VNIjODyKL/Lp0Pw174+QfEfL5tlE'
# secretKey = 'K+TlwCDi7M19hfF2RSJ51QcOqokvEy9cVSYkijmthmMnkXhAb6AwL/8o10Sxxkob'
#
# timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
# method    = 'POST'
# endPoint  = 'https://api.coin.z.com/private'
# path      = '/v1/ws-auth'
# reqBody = {}
#
# text = timestamp + method + path + json.dumps(reqBody)
# sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
#
# headers = {
#     "API-KEY": apiKey,
#     "API-TIMESTAMP": timestamp,
#     "API-SIGN": sign
# }
#
# res = requests.post(endPoint + path, headers=headers, data=json.dumps(reqBody))
# print (json.dumps(res.json(), indent=2))



