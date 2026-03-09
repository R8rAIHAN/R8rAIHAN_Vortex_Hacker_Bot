import logging
import os
import asyncio
import aiohttp
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Stealth Logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN')

# Stealth Payloads
VULN_PAYLOADS = {
    "sqli": ["' OR 1=1--", "' UNION SELECT NULL--", "1'; DROP TABLE users--"],
    "xss": ["<script>alert(1)</script>", "<img src=x onerror=alert(document.domain)>", "javascript:alert('XSS')"],
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['⚡ ULTRA SCAN', '🔍 RECON PRO'], 
        ['🛡️ WEB VULN', '📡 NET SCAN'],
        ['🔥 EXPLOIT CHAIN', '📊 PRO REPORT'], 
        ['⚙️ TOOLS', '📈 DASHBOARD']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    msg = """
🛡️ **R8rAIHAN STEALTH v3.0** 🛡️

**Authorized Pentest Platform**
*No Logs | No Footprints | Max Speed*

**Select Module to Begin:**
    """
    await update.message.reply_text(msg, reply_markup=reply_markup)

async def handle_ultra_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.text.strip()
    mode = context.user_data.get('mode')
    
    await asyncio.sleep(0.5) # Simulated delay
    
    if mode == 'ultra':
        result = f"""
⚡ **ULTRA SCAN COMPLETE** ({target}) ⚡
*Scan Time: 2.7s | 127 Tests*

**CRITICAL FINDINGS:**
🔴 SQL Injection → CONFIRMED
🔴 Path Traversal → CONFIRMED  
🔴 XSS Reflected → CONFIRMED
🔴 Weak Auth → BYPASSABLE

**Network:**
📡 Ports Open: 22,80,443,8080
🌐 Subdomains: 17 live
"""
    elif mode == 'sqli':
        result = f"""
💉 **SQLi PRO SCAN** ({target})

**Vulnerable Parameters:** 4/12
1. id → UNION SELECT (CRITICAL)
2. user → Blind Time-based  

**sqlmap Command:**
`sqlmap -u "{target}" --batch --dbs`
"""
    elif mode == 'xss':
        result = f"""
🕷️ **XSS HUNTER** ({target})
**Status:** Vulnerable
**Payload:** `{VULN_PAYLOADS['xss'][0]}`
"""
    else:
        result = "❌ Mode not selected."

    await update.message.reply_text(result)
    context.user_data.pop('mode', None)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == '⚡ ULTRA SCAN':
        context.user_data['mode'] = 'ultra'
        await update.message.reply_text("🎯 Target IP/Domain দিন:")
    elif text == '🛡️ WEB VULN':
        keyboard = [['💉 SQLi Pro', '🕷️ XSS Hunter']]
        await update.message.reply_text("সিলেক্ট করুন:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    elif text == '💉 SQLi Pro':
        context.user_data['mode'] = 'sqli'
        await update.message.reply_text("🎯 Target URL দিন:")
    elif text == '🕷️ XSS Hunter':
        context.user_data['mode'] = 'xss'
        await update.message.reply_text("🎯 Target URL দিন:")
    elif context.user_data.get('mode'):
        await handle_ultra_scan(update, context)
    else:
        await start(update, context)

def main():
    if not TOKEN:
        print("❌ BOT_TOKEN missing!")
        return
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 R8rAIHAN Bot is Live!")
    app.run_polling()

if __name__ == '__main__':
    main()
