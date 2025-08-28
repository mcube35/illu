import websocket
import json
import hmac
import base64
import time
import requests

api_key = "4f821161-2247-4e3e-b118-bb20508c9fa5"
api_secret = "B44DCDF0D86CB24C5D0A5BCDA90E6A67"
passphrase = "Mnindex35@@"

# 1️⃣ 서버 시간 가져오기
def get_okx_server_time():
    url = "https://www.okx.com/api/v5/public/time"
    resp = requests.get(url).json()
    return int(resp['data'][0]['ts']) // 1000  # ms -> s

# 2️⃣ 서명 생성
def sign(timestamp, method, request_path, body=""):
    msg = f"{timestamp}{method}{request_path}{body}"
    signature = hmac.new(api_secret.encode(), msg.encode(), digestmod="sha256").digest()
    return base64.b64encode(signature).decode()

# 3️⃣ 메시지 처리
def on_message(ws, message):
    data = json.loads(message)
    # 로그인 성공
    if 'event' in data and data['event'] == 'login' and data.get('code') == 0:
        print("Login successful ✅")
        # positions 채널 구독
        ws.send(json.dumps({
            "op": "subscribe",
            "args": [{"channel": "positions"}]
        }))
    # positions 데이터 수신
    elif 'arg' in data and data['arg']['channel'] == 'positions':
        print("New positions data:", data['data'])
    else:
        print("Other message:", data)

def on_open(ws):
    ts = str(get_okx_server_time())
    auth = {
        "op": "login",
        "args": [
            {
                "apiKey": api_key,
                "passphrase": passphrase,
                "timestamp": ts,
                "sign": sign(ts, "GET", "/users/self/verify")
            }
        ]
    }
    ws.send(json.dumps(auth))

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed:", close_status_code, close_msg)

# 4️⃣ WebSocket 실행
ws = websocket.WebSocketApp(
    "wss://ws.okx.com:8443/ws/v5/private",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()

