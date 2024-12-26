import requests
import time
import hmac
import hashlib

base_url = "https://api.coin.z.com/private"
endpoint = "/v1/account/assets"
api_key = "/delhCEiMxu1fOCfkpWW+YHZbWPqnSkd"
secret_key = "oBYdRnHolCnjHdW2YEHcw5BXtvw2DTZ3uvrWa5ONHZ2olpLjtV93FaryhgApxvlA"

timestamp = str(int(time.time()))
method = "GET"
body = ""  # GETの場合は空文字

# シグネチャ生成
text = timestamp + method + endpoint + body
signature = hmac.new(secret_key.encode('utf-8'),
                     text.encode('utf-8'),
                     hashlib.sha256
                    ).hexdigest()

headers = {
    "API-KEY": api_key,
    "API-TIMESTAMP": timestamp,
    "API-SIGN": signature
}

res = requests.get(base_url + endpoint, headers=headers)
if res.status_code == 200:
    print("Private REST 接続成功:", res.json())
else:
    print("Private REST 接続失敗:", res.text)


# プライベートAPIのエンドポイント
# HTTPS エンドポイント: https://api.coin.z.com/private
# このエンドポイントは、APIキーによる認証が必要なプライベートな情報にアクセスするために使用されます12。
# 以下のエンドポイントが提供されています。
# /v1/account/margin: 余力情報を取得します34。
# /v1/account/tradingVolume: 取引高情報を取得します5。
# /v1/orders: 指定した注文IDの注文情報を取得します67。
# /v1/activeOrders: 有効注文の一覧を取得します89。
# /v1/executions: 約定情報を取得します1011。
# /v1/latestExecutions: 最新の約定一覧を取得します1213。
# /v1/openPositions: 建玉の一覧を取得します1415。
# /v1/positionSummary: 建玉サマリーを取得します16。
# /v1/closeOrder: 決済注文をします1718。
# /v1/closeBulkOrder: 一括決済注文をします19。
# /v1/changeLosscutPrice: 建玉のロスカットレート変更をします2021。
# /v1/cancelOrder: 注文のキャンセルをします22。
# /v1/cancelOrders: 複数の注文のキャンセルをします23。
# /v1/cancelBulkOrder: 注文の一括キャンセルをします24。
# /v1/changeOrder: 注文の変更をします25。
# /v1/ws-auth: Private WebSocket API用のアクセストークンを取得、延長、削除します20262728。
# 口座振替、日本円の入金・出金履歴、暗号資産の預入・送付履歴などの機能も提供されています29。