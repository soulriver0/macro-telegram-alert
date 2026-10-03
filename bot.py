import requests

BOT_TOKEN = "8704052915:AAHJy82yFQp7ieSVu1DGD8GMGKFdWyw5-Y4"
CHAT_ID = "5052804815"

message = "✅ Telegram 봇 연결 성공!\n\n이제 시장 모니터링 시스템을 만들 준비가 됐습니다."

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)
