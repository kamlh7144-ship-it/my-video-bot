import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- 1. سيرفر وهمي للبقاء حياً (هذا قلب الحل) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Alive")

def run_health_server():
    # بورت 8080 هو البورت القياسي اللي يراقبه Koyeb
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

# --- 2. إعدادات البوت ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711
TARGET_USER_ID = 2034540192

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا علي! بوتك شغال هسة وما ينام 🚀 دز رابط وتوكل.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    if text.startswith("http"):
        if user.id == TARGET_USER_ID:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"🎯 عبود دز رابط: {text}")
        
        await update.message.reply_text("⏳ جاي أحمل...")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': f'file_{user.id}.%(ext)s', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)
            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.message.chat_id, video=f)
            with open(filename, 'rb') as f:
                await context.bot.send_voice(chat_id=update.message.chat_id, voice=f)
            os.remove(filename)
        except:
            await update.message.reply_text("❌ خطأ بالتحميل!")
    else:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 من {user.first_name}: {text}")

if __name__ == '__main__':
    # تشغيل المنبه في خلفية البوت
    threading.Thread(target=run_health_server, daemon=True).start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

