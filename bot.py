import telegram
from binance.client import Client
import time
import os

# ตั้งค่า Token ของ Bot ที่ได้รับจาก BotFather
token = os.environ['6192574289:AAECF5_PZ9cMNswsLWsDVNLrP6uCofRObjg']

# ตั้งค่า API Key และ Secret Key ของ Binance
api_key = os.environ['wh2YyosKLY4YJLrSbn1oujeEGsD7SZ8vM7CqEBPuVpdYmtBulFzLqSVM7CeJzmBa']
api_secret = os.environ['6192574289:AAECF5_PZ9cMNswsLWsDVNLrP6uCofRObjg']


# สร้าง Client สำหรับเชื่อมต่อกับ Binance
client = Client(api_key, api_secret)

# สร้าง Bot โดยใช้ Token ของ Bot ที่ได้รับจาก BotFather
bot = telegram.Bot(token)

# ฟังก์ชันสำหรับแสดงข้อมูลการซื้อขายล่าสุดของคู่สินค้าที่กำหนด
def get_latest_trade(pair):
    trades = client.get_my_trades(symbol=pair)
    latest_trade = trades[-1]
    return latest_trade

# ฟังก์ชันสำหรับแสดงข้อมูลความเคลื่อนไหวของเงินต้นเงินปัจจุบัน และกำไร / ขาดทุนทั้งหมด
def get_balance_info():
    account_info = client.get_account()
    balance = float(account_info['totalWalletBalance'])
    avail_balance = float(account_info['availableBalance'])
    pnl = float(account_info['totalUnrealizedProfit'])
    total_pnl = float(account_info['totalProfit'])
    return balance, avail_balance, pnl, total_pnl

# ฟังก์ชันสำหรับแสดงข้อมูล Drawdown Percent
def get_drawdown_info():
    account_info = client.get_account()
    balance = float(account_info['totalWalletBalance'])
    max_balance = float(account_info['maxWithdrawAmount'])
    drawdown_percent = ((max_balance - balance) / max_balance) * 100
    return drawdown_percent

# ฟังก์ชันสำหรับส่งข้อความไปยังช่องทาง Telegram ที่กำหนด
def send_message(message, chat_id):
    bot.send_message(chat_id=chat_id, text=message)

# ฟังก์ชันสำหรับเรียกดูข้อมูลและส่งข้อความไปยังช่องทาง Telegram ที่กำหนด
def check_and_send_updates(chat_id, pair):
    latest_trade = get_latest_trade(pair)
    balance, avail_balance, pnl, total_pnl = get_balance_info()
    drawdown_percent = get_drawdown_info()
    message = f"Pair: {pair}\n" \
              f"Latest Trade: {latest_trade['time']} - {latest_trade['side']} {latest_trade['qty']} {pair} @ {latest_trade['price']}\n" \
              f"Total Wallet Balance: {balance:.2f} USDT\n" \
              f"Available Balance: {avail_balance:.2f} USDT\n" \
              f"Floating PnL: {pnl:.2f} USDT\n" \
              f"Total PnL: {total_pnl:.2f} USDT\n" \
              f"Drawdown Percent: {drawdown_percent:.2f}%"
    send_message(message, chat_id)

# รันโปรแกรม
if __name__ == '__main__':
    chat_id = "@killerxyz"
    pair = "APEUSDT"
    while True:
        check_and_send_updates(chat_id, pair)
        time.sleep(60) # ตั้งค่าเวลาในการเช็คและส่งข้อมูลใหม่ทุก ๆ 1 นาที
