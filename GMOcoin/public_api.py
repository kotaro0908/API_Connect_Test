import requests

base_url = "https://api.coin.z.com/public"
endpoint = "/v1/status"  # 他のエンドポイントでもOK

res = requests.get(base_url + endpoint)
if res.status_code == 200:
    print("Public REST 接続成功:", res.json())
else:
    print("Public REST 接続失敗:", res.text)

#●HTTPS エンドポイント: https://api.coin.z.com/public
#このエンドポイントは、認証不要で利用できる静的な情報を取得するために使用されます。
#以下のエンドポイントが提供されています。
#/v1/status: 取引所の稼働状態を取得します。
#/v1/ticker: 指定した銘柄の最新レートを取得します。symbolパラメータを指定しない場合は、全銘柄の最新レートが返されます。
#/v1/orderbooks: 指定した銘柄の板情報を取得します。symbolパラメータは必須です。
#/v1/trades: 指定した銘柄の取引履歴を取得します。symbolパラメータは必須です。
#/v1/symbols: 取扱銘柄の一覧を取得します。
