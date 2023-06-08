import telegram
from telegram.ext import Updater
from binance.client import Client

# กำหนด Token ของ Telegram bot ที่ได้รับจาก BotFather
TELEGRAM_BOT_TOKEN = '6192574289:AAECF5_PZ9cMNswsLWsDVNLrP6uCofRObjg'

# กำหนด API Key และ Secret Key ของ Binance
BINANCE_API_KEY = 'wh2YyosKLY4YJLrSbn1oujeEGsD7SZ8vM7CqEBPuVpdYmtBulFzLqSVM7CeJzmBa'
BINANCE_SECRET_KEY = '9s4LGdWGZKmWns33N9wMcYfJHGwRPbLswerbwWRDLsZWLfhjFeGUkgeFMZcxIkCA'

# สร้างตัวแปรสำหรับเก็บ chat_id ของผู้ใช้งาน
chat_id = None

# กำหนด function สำหรับคำสั่ง /start
def start(update, context):
    global chat_id
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="สวัสดีค่ะ ยินดีต้อนรับสู่บอทของเรา")

# กำหนด function สำหรับคำสั่ง /monitor
def monitor(update, context):
    context.bot.send_message(chat_id=chat_id, text="กำลังเริ่มต้นการตรวจสอบตำแหน่ง Future โปรดรอสักครู่...")

    # สร้างตัวเชื่อมต่อกับ Binance API
    client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)

    # ดึงข้อมูลตำแหน่ง Future จาก Binance API
    futures_positions = client.futures_position_information()

    # ตรวจสอบตำแหน่งที่เปิดและปิด
    opened_positions = []
    closed_positions = []

    for position in futures_positions:
        if float(position['positionAmt']) != 0.0:
            if float(position['entryPrice']) == 0.0:
                closed_positions.append(position)
            else:
                opened_positions.append(position)

    # ส่งข้อมูลการเปิดและปิดตำแหน่ง Future ไปยังผู้ใช้งาน
    if opened_positions:
        opened_positions_text = '\n'.join([f"Symbol: {position['symbol']}, Position: {position['positionAmt']}" for position in opened_positions])
        context.bot.send_message(chat_id=chat_id, text=f"ตำแหน่ง Future ที่เปิด:\n{opened_positions_text}")
    else:
        context.bot.send_message(chat_id=chat_id, text="ไม่มีตำแหน่ง Future ที่เปิด")

    if closed_positions:
        closed_positions_text = '\n'.join([f"Symbol: {position['symbol']}, Position: {position['positionAmt']}" for position in closed_positions])
        context.bot.send_message(chat_id=chat_id, text=f"ตำแหน่ง Future ที่ปิด:\n{closed_positions_text}")
    else:
        context.bot.send_message(chat_id=chat_id, text="ไม่มีตำแหน่ง Future ที่ปิด")

# กำหนด function สำหรับคำสั่ง /help
def help(update, context):
    help_text = """
    สวัสดีค่ะ นี่คือคำสั่งที่สามารถใช้ได้กับบอทของเรา:
    /start - เริ่มต้นการใช้งานบอท
    /monitor - ตรวจสอบตำแหน่ง Future ที่เปิดและปิด
    /help - แสดงคำสั่งทั้งหมดที่สามารถใช้ได้
    """
    context.bot.send_message(chat_id=chat_id, text=help_text)

# กำหนด function สำหรับคำสั่งไม่รู้จัก
def unknown(update, context):
    context.bot.send_message(chat_id=chat_id, text="ขออภัยค่ะ ฉันไม่เข้าใจคำสั่งนี้")

# กำหนด Token ของ Telegram bot และสร้าง updater
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

# กำหนดคำสั่งให้กับ handler
start_handler = CommandHandler('start', start)
monitor_handler = CommandHandler('monitor', monitor)
help_handler = CommandHandler('help', help)
unknown_handler = MessageHandler(telegram.ext.Filters.command, unknown)

# เพิ่ม handler เข้ากับ updater
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(monitor_handler)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(unknown_handler)

# เริ่มการทำงานของบอท
updater.start_polling()
updater.idle()
