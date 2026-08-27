#!/usr/bin/env python3
"""
MASTER API SEARCH BOT
All Lynx APIs integrated into Telegram Bot
Powered By @Introspection007
"""

import os
import json
import re
import requests
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# ============================================================
# CONFIGURATION
# ============================================================
TOKEN = "8786109822:AAFEPEAkOyUuUyFER_ufCfeyGyvnzFtfEcA"
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
# FORMAT RESULT FOR TELEGRAM
# ============================================================
def format_result(text, max_length=4000):
    if len(text) > max_length:
        return text[:max_length] + "\n\n... (truncated)"
    return text

# ============================================================
# BOT HANDLERS
# ============================================================

# ---- MAIN MENU BUTTONS ----
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

# ---- START ----
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

# ---- ABOUT ----
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

# ---- BUTTON HANDLER ----
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

# ---- MESSAGE HANDLER ----
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    search_type = context.user_data.get('search_type', 'num')
    
    # Show typing indicator
    await update.message.chat.send_action(action="typing")
    
    # Validate input based on search type
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
    
    # Show processing message
    msg = await update.message.reply_text("⏳ Searching... Please wait.")
    
    # Perform search
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
    
    # Delete processing message
    await msg.delete()
    
    # Send result
    formatted_result = format_result(result)
    await update.message.reply_text(
        f"📊 **Search Results**\n\n{formatted_result}\n\n---\n⚡ Powered By @Introspection007",
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

# ---- CANCEL ----
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled. Use /start to begin again.", reply_markup=get_main_menu())
    return ConversationHandler.END

# ============================================================
# MAIN
# ============================================================
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Conversation handler
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
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(conv_handler)
    
    print("🤖 MASTER API SEARCH BOT STARTED")
    print("⚡ Powered By @Introspection007")
    print("=" * 40)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
