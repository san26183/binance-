import os
from binance.client import Client
from telegram.ext import Updater, CommandHandler

# ตั้งค่า API Key และ API Secret ของ Binance
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# ตั้งค่า token ของ Telegram bot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
updater = Updater(token=BOT_TOKEN, use_context=True)

def binance_info(update, context):
    # ดึงข้อมูลของบัญชี
    account_info = client.futures_account()
    total_wallet_balance = float(account_info['totalWalletBalance'])
    available_balance = float(account_info['availableBalance'])
    margin_level = float(account_info['marginLevel'])
    unrealized_pnl = float(account_info['totalUnrealizedProfit'])
    total_realized_pnl = float(account_info['totalMarginRealizedProfit'])
    total_balance = float(account_info['totalMarginBalance'])
    drawdown_percent = (total_balance - total_wallet_balance) / total_balance * 100
    
    # ส่งข้อมูลไปยัง Telegram bot
    message = f'ข้อมูลบัญชี Binance:\n'
    message += f'Capital: {total_wallet_balance}\n'
    message += f'Balance: {total_balance}\n'
    message += f'Available Balance: {available_balance}\n'
    message += f'Floating PNL: {unrealized_pnl}\n'
    message += f'Total Realized PNL: {total_realized_pnl}\n'
    message += f'Drawdown Percent: {drawdown_percent:.2f}%\n'
    message += f'Margin Level: {margin_level:.2f}%\n'
    update.message.reply_text(message)

# กำหนดคำสั่ง "/binance_info"
updater.dispatcher.add_handler(CommandHandler('binance_info', binance_info))

# เริ่มต้นรับข้อมูล
updater.start_polling()
