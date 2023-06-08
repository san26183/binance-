import telegram
from telegram.ext import Updater, CommandHandler
from binance.client import Client

# กำหนด Token ของ Telegram bot ที่ได้รับจาก BotFather
TELEGRAM_BOT_TOKEN = '6192574289:AAECF5_PZ9cMNswsLWsDVNLrP6uCofRObjg'

# กำหนด API Key และ Secret Key ของ Binance
BINANCE_API_KEY = 'wh2YyosKLY4YJLrSbn1oujeEGsD7SZ8vM7CqEBPuVpdYmtBulFzLqSVM7CeJzmBa'
BINANCE_SECRET_KEY = '9s4LGdWGZKmWns33N9wMcYfJHGwRPbLswerbwWRDLsZWLfhjFeGUkgeFMZcxIkCA'

# สร้าง client สำหรับการเชื่อมต่อกับ Binance API
client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)

# กำหนด function สำหรับคำสั่ง /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="สวัสดีค่ะ ยินดีต้อนรับสู่บอทของเรา")

# กำหนด function สำหรับคำสั่ง /capital
def capital(update, context):
    # ดึงข้อมูล capital จาก Binance API
    capital = client.get_account()["totalAssetOfBtc"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Capital: {capital} BTC")

# กำหนด function สำหรับคำสั่ง /balance
def balance(update, context):
    # ดึงข้อมูล balance จาก Binance API
    balance = client.get_account()["balances"]
    balance_text = "\n".join([f"{asset['asset']}: {asset['free']}" for asset in balance])
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Balance:\n{balance_text}")

# กำหนด function สำหรับคำสั่ง /availbalance
def avail_balance(update, context):
    # ดึงข้อมูล available balance จาก Binance API
    avail_balance = client.get_account()["balances"]
    avail_balance_text = "\n".join([f"{asset['asset']}: {asset['free']}" for asset in avail_balance if float(asset['free']) > 0])
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Available Balance:\n{avail_balance_text}")

# กำหนด function สำหรับคำสั่ง /floatingpnl
def floating_pnl(update, context):
    # ดึงข้อมูล floating PNL จาก Binance API
    floating_pnl = client.futures_account()["totalUnrealizedProfit"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Floating PNL: {floating_pnl}")

# กำหนด function สำหรับคำสั่ง /drawdownpercent
def drawdown_percent(update, context):
    # คำนวณ drawdown percent จาก Binance API
    # โค้ดคำนวณได้ตามความต้องการ

# กำหนด function สำหรับคำสั่ง /totalprofit
def total_profit(update, context):
    # คำนวณ total profit จาก Binance API
    # โค้ดคำนวณได้ตามความต้องการ

# กำหนด function สำหรับคำสั่ง /help
def help(update, context):
    help_text = """
    สวัสดีค่ะ นี่คือคำสั่งที่สามารถใช้ได้กับบอทของเรา:
    /start - เริ่มต้นการใช้งาน
    /capital - แสดงข้อมูล capital
    /balance - แสดงข้อมูล balance
    /availbalance - แสดงข้อมูล available balance
    /floatingpnl - แสดงข้อมูล floating PNL
    /drawdownpercent - แสดงข้อมูล drawdown percent
    /totalprofit - แสดงข้อมูล total profit
    /help - แสดงคำสั่งทั้งหมดที่สามารถใช้ได้
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

# กำหนด function สำหรับคำสั่งไม่รู้จัก
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ขออภัยค่ะ ฉันไม่เข้าใจคำสั่งนี้")

# กำหนด Token ของ Telegram bot และสร้าง updater
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

# กำหนดคำสั่งให้กับ handler
start_handler = CommandHandler('start', start)
capital_handler = CommandHandler('capital', capital)
balance_handler = CommandHandler('balance', balance)
avail_balance_handler = CommandHandler('availbalance', avail_balance)
floating_pnl_handler = CommandHandler('floatingpnl', floating_pnl)
drawdown_percent_handler = CommandHandler('drawdownpercent', drawdown_percent)
total_profit_handler = CommandHandler('totalprofit', total_profit)
help_handler = CommandHandler('help', help)
unknown_handler = MessageHandler(Filters.command, unknown)

# เพิ่ม handler เข้ากับ updater
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(capital_handler)
updater.dispatcher.add_handler(balance_handler)
updater.dispatcher.add_handler(avail_balance_handler)
updater.dispatcher.add_handler(floating_pnl_handler)
updater.dispatcher.add_handler(drawdown_percent_handler)
updater.dispatcher.add_handler(total_profit_handler)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(unknown_handler)

# เริ่มการทำงานของบอท
updater.start_polling()
updater.idle()
