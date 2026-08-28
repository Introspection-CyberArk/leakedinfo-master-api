#!/usr/bin/env python3
"""
MASTER API SEARCH BOT - Vercel Edition
All Lynx APIs integrated into Telegram Bot
Powered By @Introspection007
"""

import os
import json
import re
import requests
import urllib.parse
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# ============================================================
# CONFIGURATION
# ============================================================
TOKEN = os.environ.get('TELEGRAM_TOKEN', '8786109822:AAFEPEAkOyUuUyFER_ufCfeyGyvnzFtfEcA')
BOT_USERNAME = "@Introspection007"

# Conversation states
SELECTING_SEARCH, WAITING_PHONE, WAITING_ADDRESS, WAITING_NAME, WAITING_AADHAR = range(5)

# ============================================================
# SAFE JSON PARSER
# ============================================================
def parse_json_safely(text):
    try:
        return json.loads(text)
    except:
        pass
    match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    try:
        decoder = json.JSONDecoder()
        data, _ = decoder.raw_decode(text)
        return data
    except:
        pass
    return None

# ============================================================
# API FUNCTIONS
# ============================================================

def search_hitek(number):
    url = f"https://lynx.mireiariosss.workers.dev/api/chain/{number}"
    try:
        resp = requests.get(url, timeout=30)
        data = parse_json_safely(resp.text)
        if data:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return "❌ No data found"
    except Exception as e:
        return f"❌ Error: {e}"

def search_num(number):
    url = f"https://lynx.mireiariosss.workers.dev/api/search/{number}"
    try:
        resp = requests.get(url, timeout=30)
        data = parse_json_safely(resp.text)
        if data and data.get('success'):
            results = data.get('results', [])
            if not results:
                return "❌ No results found"
            output = f"✅ Found {len(results)} result(s):\n\n"
            for i, r in enumerate(results, 1):
                output += f"""
📌 [{i}]
📱 Mobile: {r.get('mobile', 'N/A')}
👤 Name: {r.get('name', 'N/A')}
👨 Father: {r.get('father_name', 'N/A')}
📍 Address: {r.get('address', 'N/A')}
📡 Circle: {r.get('circle', 'N/A')}
🆔 Aadhar: {r.get('aadhar', 'N/A')}
📧 Email: {r.get('email', 'N/A')}
{'─' * 30}
"""
            return output
        return "❌ No results found"
    except Exception as e:
        return f"❌ Error: {e}"

def search_address(address):
    encoded = urllib.parse.quote(address)
    url = f"https://lynx.mireiariosss.workers.dev/api/address/{encoded}"
    try:
        resp = requests.get(url, timeout=30)
        data = parse_json_safely(resp.text)
        if data:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return "❌ No data found"
    except Exception as e:
        return f"❌ Error: {e}"

def search_icmr_phone(number):
    url = f"https://lynx.mireiariosss.workers.dev/api/icmr/phone/{number}"
    try:
        resp = requests.get(url, timeout=30)
        data = parse_json_safely(resp.text)
        if data:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return "❌ No data found"
    except Exception as e:
        return f"❌ Error: {e}"

def search_icmr_name(name):
    url = f"https://lynx.mireiariosss.workers.dev/api/icmr/name/{name}"
    try:
        resp = requests.get(url, timeout=30)
        data = parse_json_safely(resp.text)
        if data:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return "❌ No data found"
    except Exception as e:
        return f"❌ Error: {e}"

def search_icmr_aadhar(aadhar):
    url = f"https://lynx.mireiariosss.workers.dev/api/icmr/aadhar/{aadhar}"
    try:
        resp = requests.get(url, timeout=30)
        data = parse_json_safely(resp.text)
        if data:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return "❌ No data found"
    except Exception as e:
        return f"❌ Error: {e}"

def search_all(query):
    output = "🚀 SEARCHING ALL APIS\n" + "=" * 30 + "\n\n"
    output += "🔍 NUM SEARCH:\n" + search_num(query) + "\n\n"
    output += "🔗 HITEK CHAIN:\n" + search_hitek(query) + "\n\n"
    output += "🇮🇳 ICMR PHONE:\n" + search_icmr_phone(query)
    return output

# ============================================================
# BOT HANDLERS
# ============================================================

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🔗 Hitek Chain", callback_data="hitek")],
        [InlineKeyboardButton("❤️‍🔥 Num Search", callback_data="num")],
        [InlineKeyboardButton("📍 Address Search", callback_data="address")],
        [InlineKeyboardButton("🇮🇳 ICMR Phone", callback_data="icmr_phone")],
        [InlineKeyboardButton("📛 ICMR Name", callback_data="icmr_name")],
        [InlineKeyboardButton("👨‍🦰 ICMR Aadhar", callback_data="icmr_aadhar")],
        [InlineKeyboardButton("🚀 SEARCH ALL", callback_data="all")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome = f"""
🤖 MASTER API SEARCH BOT

Welcome {user.first_name}! 👋

🔍 Search across multiple APIs:
• 🔗 Hitek Chain
• ❤️‍🔥 Num Search  
• 📍 Address Search
• 🇮🇳 ICMR (Phone/Name/Aadhar)
• 🚀 Search ALL at once

Select an option below:

---
⚡ Powered By @Introspection007
"""
    await update.message.reply_text(welcome, reply_markup=get_main_menu())

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    about_text = """
ℹ️ ABOUT THIS BOT

🔍 Master API Search Bot
📡 All Lynx APIs integrated

Available APIs:
• Hitek Chain (Phone)
• Num Search (Phone)
• Address Search
• ICMR Phone
• ICMR Name
• ICMR Aadhar

🚀 Search ALL with one click

---
⚡ Powered By @Introspection007
"""
    await query.edit_message_text(about_text, reply_markup=get_main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "about":
        await about(update, context)
        return
    
    search_types = {
        "hitek": {"text": "🔗 Enter phone number for Hitek Chain:", "state": WAITING_PHONE, "type": "hitek"},
        "num": {"text": "❤️‍🔥 Enter phone number for Num Search:", "state": WAITING_PHONE, "type": "num"},
        "address": {"text": "📍 Enter full address to search:", "state": WAITING_ADDRESS, "type": "address"},
        "icmr_phone": {"text": "🇮🇳 Enter phone number for ICMR:", "state": WAITING_PHONE, "type": "icmr_phone"},
        "icmr_name": {"text": "📛 Enter name for ICMR:", "state": WAITING_NAME, "type": "icmr_name"},
        "icmr_aadhar": {"text": "👨‍🦰 Enter 12-digit Aadhar number:", "state": WAITING_AADHAR, "type": "icmr_aadhar"},
        "all": {"text": "🚀 Enter phone number to search ALL APIs:", "state": WAITING_PHONE, "type": "all"},
    }
    
    if data in search_types:
        context.user_data['search_type'] = data
        await query.edit_message_text(
            search_types[data]["text"],
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
        )
        return search_types[data]["state"]
    
    if data == "back":
        await query.edit_message_text("🔍 Select a search option:", reply_markup=get_main_menu())
        return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    search_type = context.user_data.get('search_type', 'num')
    
    await update.message.chat.send_action(action="typing")
    
    if search_type in ["hitek", "num", "icmr_phone", "all"]:
        if not user_input.isdigit() or len(user_input) < 10:
            await update.message.reply_text(
                "❌ Invalid phone number! Please enter a valid 10-digit number.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
            )
            return WAITING_PHONE
    
    if search_type == "icmr_aadhar":
        if not user_input.isdigit() or len(user_input) != 12:
            await update.message.reply_text(
                "❌ Invalid Aadhar! Please enter a valid 12-digit Aadhar number.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
            )
            return WAITING_AADHAR
    
    msg = await update.message.reply_text("⏳ Searching... Please wait.")
    
    if search_type == "hitek":
        result = search_hitek(user_input)
    elif search_type == "num":
        result = search_num(user_input)
    elif search_type == "address":
        result = search_address(user_input)
    elif search_type == "icmr_phone":
        result = search_icmr_phone(user_input)
    elif search_type == "icmr_name":
        result = search_icmr_name(user_input)
    elif search_type == "icmr_aadhar":
        result = search_icmr_aadhar(user_input)
    elif search_type == "all":
        result = search_all(user_input)
    else:
        result = "❌ Unknown search type"
    
    await msg.delete()
    
    formatted_result = result[:4000]  # Telegram max length
    await update.message.reply_text(
        f"📊 **Search Results**\n\n{formatted_result}\n\n---\n⚡ Powered By @Introspection007",
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled. Use /start to begin again.", reply_markup=get_main_menu())
    return ConversationHandler.END

# ============================================================
# FLASK APP FOR WEBHOOK
# ============================================================
app = Flask(__name__)

# Initialize Application and bot
application = Application.builder().token(TOKEN).build()

# Register handlers
conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler)],
    states={
        WAITING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        WAITING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        WAITING_AADHAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", start))
application.add_handler(conv_handler)

@app.route('/', methods=['GET'])
def index():
    return "🤖 API Search Bot is running! Powered By @Introspection007"

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle incoming Telegram updates"""
    try:
        # Get the update data
        update_data = request.get_json()
        if not update_data:
            return jsonify({"status": "error", "message": "No data"}), 400

        # Create Update object
        update = Update.de_json(update_data, application.bot)

        # Process the update
        await application.process_update(update)

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error in webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============================================================
# SET WEBHOOK ON STARTUP
# ============================================================
def set_webhook():
    """Set the webhook URL for Telegram"""
    # Get the base URL from environment (Vercel provides this)
    vercel_url = os.environ.get('VERCEL_URL')
    if vercel_url:
        webhook_url = f"https://{vercel_url}/webhook"
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/setWebhook",
                json={"url": webhook_url}
            )
            if response.ok:
                print(f"✅ Webhook set to {webhook_url}")
            else:
                print(f"❌ Failed to set webhook: {response.text}")
        except Exception as e:
            print(f"❌ Error setting webhook: {e}")

# Set webhook when app starts (Vercel serverless)
set_webhook()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
