import os
from binance.client import Client
from telegram.ext import Updater, CommandHandler

binance_api_key = os.environ.get('BINANCE_API_KEY')
binance_api_secret = os.environ.get('BINANCE_API_SECRET')

client = Client(binance_api_key=binance_api_key, binance_api_secret=binance_api_secret)

# สร้างฟังก์ชันเพื่อดึงข้อมูล balance และ available balance
def get_balance(update, context):
    balance = client.get_asset_balance(asset='USDT')
    avail_balance = client.get_asset_balance(asset='USDT')['free']
    update.message.reply_text(f"Balance: {balance['free']} USDT\nAvailable Balance: {avail_balance} USDT")

# สร้างฟังก์ชันเพื่อดึงข้อมูล capital
def get_capital(update, context):
    account = client.futures_account()
    balance = account['totalWalletBalance']
    update.message.reply_text(f"Total capital: {balance} USDT")

# สร้างฟังก์ชันเพื่อดึงข้อมูล floating PnL
def get_floating_pnl(update, context):
    positions = client.futures_position_information()
    floating_pnl = 0
    for position in positions:
        if position['symbol'] == 'BTCUSDT':
            floating_pnl += float(position['unRealizedProfit'])
    update.message.reply_text(f"Floating PnL: {floating_pnl} USDT")

# สร้างฟังก์ชันเพื่อดึงข้อมูล drawdown percent
def get_drawdown(update, context):
    account = client.futures_account()
    initial_balance = float(account['totalInitialMargin'])
    current_balance = float(account['totalWalletBalance'])
    drawdown = (initial_balance - current_balance) / initial_balance * 100
    update.message.reply_text(f"Drawdown: {drawdown:.2f}%")

# สร้างฟังก์ชันเพื่อดึงข้อมูล total profit
def get_total_profit(update, context):
    account = client.futures_account()
    total_profit = float(account['totalUnrealizedProfit']) + float(account['totalMarginBalance']) - float(account['totalWalletBalance'])
    update.message.reply_text(f"Total Profit: {total_profit} USDT")

# สร้างฟังก์ชันเพื่อดึงข้อมูลของ future trade ทั้งหมด
def get_future_trades(update, context):
    trades = client.futures_account_trades()
    for trade in trades:
        update.message.reply_text(f"{trade['symbol']}, {trade['time']}, {trade['side']}, {trade['price']}, {trade['qty']}")

# สร้าง Telegram bot และเชื่อมต่อกับฟังก์ชัน
updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('balance', get_balance))
dispatcher.add_handler(CommandHandler('capital', get_capital))
dispatcher.add_handler(CommandHandler('floating_pnl', get_floating_pnl))
dispatcher.add_handler(CommandHandler('drawdown', get_drawdown))
dispatcher.add_handler(CommandHandler('total_profit', get_total_profit))
dispatcher.add_handler(CommandHandler('future_trades', get_future_trades))

# เริ่มต้นการทำงานของ Telegram bot
updater.start_polling()
updater.idle()
