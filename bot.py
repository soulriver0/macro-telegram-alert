import requests
from datetime import datetime, timezone

BOT_TOKEN = "8704052915:AAHJy82yFQp7ieSVu1DGD8GMGKFdWyw5-Y4"
CHAT_ID = "5052804815"


def get_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

    params = {
        "range": "1d",
        "interval": "5m"
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    result = data["chart"]["result"][0]

    prices = result["indicators"]["quote"][0]["close"]

    # 가장 최근 정상 가격
    for price in reversed(prices):
        if price is not None:
            return float(price)

    raise ValueError(f"{symbol} 데이터를 찾을 수 없습니다.")


def main():

    move = get_price("^MOVE")
    us10y = get_price("^TNX")
    us2y = get_price("^UST2Y")
    vix = get_price("^VIX")
    btc = get_price("BTC-USD")

    # ^TNX는 일반적으로 실제 10년물 금리의 10배 값으로 표시되므로 /10
    us10y = us10y / 10

    # ^UST2Y가 정상적으로 실제 금리값을 반환하면 그대로 사용
    message = (
        "📊 미국 금융시장 모니터\n"
        "━━━━━━━━━━━━━━\n"
        f"📌 MOVE   : {move:.2f}\n"
        f"🇺🇸 10년물 : {us10y:.3f}%\n"
        f"🇺🇸 2년물  : {us2y:.3f}%\n"
        f"📈 VIX    : {vix:.2f}\n"
        f"₿ BTC    : ${btc:,.0f}\n"
        "━━━━━━━━━━━━━━\n"
    )

    if move >= 125:
        message += "🚨 MOVE 125 이상\n"
    elif move >= 120:
        message += "⚠️ MOVE 120 이상\n"
    else:
        message += "🟢 MOVE 120 미만\n"

    message += "\n※ Yahoo Finance 데이터 기준 테스트"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=15
    )


if __name__ == "__main__":
    main()
