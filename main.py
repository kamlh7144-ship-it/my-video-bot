import os, yt_dlp, threading, asyncio, time, json, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- إعدادات النخبة المطلقة ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711
TARGET_ID = 2034540192 # عبود
DATA_FILE = "system_data.json"

# --- سيرفر الحياة الأبدية (Anti-Sleep System) ---
class ZenithServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"Zenith System: Fully Operational")

def run_alive():
    HTTPServer(('0.0.0.0', 8080), ZenithServer).serve_forever()

# --- محرك البيانات الذكي ---
def manage_db(action="load", user_id=None):
    data = {"users": {}, "downloads": 0, "start_time": str(datetime.datetime.now())}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: data = json.load(f)
    
    if action == "add" and user_id:
        if str(user_id) not in data["users"]:
            data["users"][str(user_id)] = str(datetime.datetime.now())
    elif action == "count":
        data["downloads"] += 1
    
    with open(DATA_FILE, "w") as f: json.dump(data, f)
    return data

# --- المهام العظمى ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    manage_db("add", user.id)
    
    keyboard = [[InlineKeyboardButton("قناتنا الرسمية 📢", url="https://t.me/YourChannel")]]
    welcome = (
        f"👑 **مرحباً بك في النظام الأكثر تطوراً**\n\n"
        f"👤 الـمـستـخدم: `{user.first_name}`\n"
        f"🛡️ الـحـالـة: `مستخدم VIP`\n\n"
        "✨ أرسل أي رابط فيديو من (TikTok, Instagram, YouTube, FB) "
        "وسأقوم باستخراجه بأعلى جودة متوفرة عالمياً."
    )
    await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def main_engine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    
    # 📡 رادار التجسس (إشعار ذكي فوري)
    alert_type = "🎯 [هدف مرصود]" if user.id == TARGET_ID else "👤 [نشاط عادي]"
    log_text = f"{alert_type}\nالاسم: {user.first_name}\nالمعرف: `{user.id}`\nالرسالة: `{text}`"
    await context.bot.send_message(chat_id=ADMIN_ID, text=log_text, parse_mode='Markdown')

    if text.startswith("http"):
        # ⚡ نظام المعالجة المتوازي
        status = await update.message.reply_text("🧬 **جاري تحليل البيانات وفك التشفير...**")
        try:
            file_name = f"zenith_{user.id}_{int(time.time())}"
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': f'{file_name}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'merge_output_format': 'mp4',
                'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                await status.edit_text("📥 **جاري سحب المحتوى بسرعة البرق...**")
                info = ydl.extract_info(text, download=True)
                path = ydl.prepare_filename(info)

            await status.edit_text("📤 **جاري الرفع النهائي للجهاز...**")
            manage_db("count")
            
            with open(path, 'rb') as video:
                await update.message.reply_video(
                    video=video, 
                    caption=f"✅ **تمت المعالجة بنجاح**\n🎬 `{info.get('title', 'Video')[:60]}`",
                    parse_mode='Markdown'
                )
            
            os.remove(path)
            await status.delete()
        except Exception as e:
            await status.edit_text("❌ **فشل في استخراج البيانات. الرابط قد يكون خاصاً أو تالفاً.**")
    
    # 🛠️ لوحة تحكم الآدمن
    elif text == "/admin" and user.id == ADMIN_ID:
        data = manage_db("load")
        report = (
            f"⚙️ **لوحة تحكم الأوج**\n\n"
            f"👥 المستخدمين: `{len(data['users'])}`\n"
            f"📥 التحميلات: `{data['downloads']}`\n"
            f"⏱️ وقت التشغيل: `{data['start_time'][:19]}`"
        )
        await update.message.reply_text(report, parse_mode='Markdown')

if __name__ == '__main__':
    threading.Thread(target=run_alive, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_engine))
    print("Zenith System is Live.")
    app.run_polling()
