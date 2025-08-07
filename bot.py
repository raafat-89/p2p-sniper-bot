import asyncio
import nest_asyncio
import requests
from datetime import datetime
from telegram import Bot
import pytz

# إعداد البيئة التزامنية داخل tmux أو Jupyter
nest_asyncio.apply()

# إعدادات البوت
BOT_TOKEN = "ضع_توكن_البوت_هنا"
CHAT_ID = "ضع_chat_id_هنا"

bot = Bot(token=BOT_TOKEN)

# العملات التي نريد مراقبتها
ASSETS = ["USDT", "BTC", "ETH"]
FIAT = ["TRY", "AED", "USD"]

# كم يجب أن يكون الخصم عن السوق ليُرسل تنبيه
REQUIRED_DISCOUNT = 5  # مثال: 5%

# عدد الثواني المقبول كحد أقصى لعمر الإعلان
MAX_AD_AGE_SECONDS = 60

# احصل على سعر السوق من Binance Spot
def get_spot_price(asset: str, fiat: str):
    try:
        symbol = asset + fiat
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url, timeout=10)
        data = res.json()
        return float(data["price"])
    except:
        return None

# إرسال رسالة لتليغرام
async def send_message(text: str):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        print(f"فشل إرسال الرسالة: {e}")

# الفحص المستمر
async def monitor():
    print("✅ البوت بدأ العمل...")
    while True:
        try:
            for asset in ASSETS:
                for fiat in FIAT:
                    spot_price = get_spot_price(asset, fiat)
                    if not spot_price:
                        continue

                    res = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", json={
                        "asset": asset,
                        "fiat": fiat,
                        "tradeType": "SELL",
                        "page": 1,
                        "rows": 1
                    }, timeout=10)

                    data = res.json()
                    adv = data["data"][0]["adv"]
                    advertiser = data["data"][0]["advertiser"]

                    if "publishTime" in adv:
                        publish_ts = int(adv["publishTime"]) / 1000
                        now_ts = datetime.now().timestamp()
                        age = now_ts - publish_ts

                        if age <= MAX_AD_AGE_SECONDS:
                            p2p_price = float(adv["price"])
                            discount = (spot_price - p2p_price) / spot_price * 100

                            if discount >= REQUIRED_DISCOUNT:
                                time_str = datetime.fromtimestamp(publish_ts, pytz.timezone("Europe/Istanbul")).strftime("%Y-%m-%d %H:%M:%S")
                                link = f"https://p2p.binance.com/tr/advertiserDetail?advertiserNo={advertiser['userNo']}"
                                msg = (
                                    f"?? <b>فرصة P2P على Binance</b>\n\n"
                                    f"?? العملة: {asset} → {fiat}\n"
                                    f"?? السعر: {p2p_price:.2f} (خصم {discount:.2f}%)\n"
                                    f"??‍?? التاجر: {advertiser['nickName']}\n"
                                    f"?? الوقت: {time_str}\n"
                                    f"?? <a href='{link}'>رابط التاجر</a>"
                                )
                                await send_message(msg)

        except Exception as e:
            await send_message(f"❌ خطأ:\n<code>{e}</code>")
            await asyncio.sleep(10)

        await asyncio.sleep(5)

# تشغيل البوت
asyncio.run(monitor())
