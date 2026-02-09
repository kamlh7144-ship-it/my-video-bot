import os, yt_dlp, threading, time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- الإعدادات ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711
TARGET_ID = 2034540192

# سيرفر الصمود
class AliveServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"System Online")

def run_alive():
    HTTPServer(('0.0.0.0', 8080), AliveServer).serve_forever()

async def handle_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    
    # التجسس (إشعار الآدمن)
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"👤 {user.first_name}: {text}")

    if "instagram.com" in text or "http" in text:
        msg = await update.message.reply_text("⛓️ **جاري كسر حماية إنستغرام وسحب الفيديو...**")
        try:
            file_id = f"ali_{int(time.time())}.mp4"
            
            ydl_opts = {
                'format': 'best', 
                'outtmpl': file_id,
                'quiet': True,
                'no_warnings': True,
                # --- السر هنا ---
                'cookiefile': 'cookies.txt',  # هذا الملف سيجعل إنستا "يخضع" للبوت
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'add_header': [
                    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept-Language: en-US,en;q=0.9',
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(text, download=True)

            await msg.edit_text("🚀 **تم الكسر! جاري الرفع...**")
            with open(file_id, 'rb') as f:
                await update.message.reply_video(video=f, caption="✅ تم التحميل غصباً عن الحماية")
            
            os.remove(file_id)
            await msg.delete()

        except Exception as e:
            await msg.edit_text("❌ **إنستغرام يرفض الطلب!**\nتحتاج لإضافة ملف `cookies.txt` بجانب الكود.")
    else:
        await update.message.reply_text("دز رابط يا وحش! 🗿")

if __name__ == '__main__':
    threading.Thread(target=run_alive, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_logic))
    app.run_polling()

