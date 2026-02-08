import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الأساسية ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    # تم تعديل الرسالة هنا حتى ما حد يدري
    await update.message.reply_text(
        f"هلا {user_name}! وياك 'علي' غول التحميل 🚀\n\n"
        "دزلي رابط (فيس، يوتيوب، تيك توك، إنستا) وراح أدزلك الفيديو وبصمة الصوت مالته سوا 🎤📹"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    # 1. إذا كانت الرسالة رابط (تحميل)
    if text.startswith("http"):
        await update.message.reply_text("جا يحمل صبر نتكم خره 🙂")
        
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'file_{user.id}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)
                
                title = info.get('title', 'فيديو بدون عنوان')
                artist = info.get('artist', info.get('uploader', 'مجهول'))

            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.message.chat_id, video=f, caption=f"✅ {title}")
            
            with open(filename, 'rb') as f:
                await context.bot.send_voice(chat_id=update.message.chat_id, voice=f, caption=f"🎤 بصمة: {artist}")
            
            os.remove(filename)
                
        except Exception as e:
            await update.message.reply_text("❌ صار خطأ.. تأكد من الرابط!")

    # 2. إذا كانت الرسالة كلام عادي (توصيل سري للمطور)
    else:
        # مسحنا الرد على المستخدم هنا.. البوت راح يسكت وما يجاوبه شي
        
        report = (
            f"📩 **رسالة سرية جديدة:**\n\n"
            f"👤 الأسم: {user.first_name}\n"
            f"🆔 الايدي: `{user.id}`\n"
            f"💬 الرسالة: {text}"
        )
        # الرسالة توصلك إلك بس
        await context.bot.send_message(chat_id=ADMIN_ID, text=report, parse_mode='Markdown')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
