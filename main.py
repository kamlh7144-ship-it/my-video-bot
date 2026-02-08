import os
import yt_dlp
from telegram.ext import Application, MessageHandler, filters

# التوكن مالتك صحيح وشغال
TOKEN = "8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI"

async def download_video(update, context):
    url = update.message.text
    await update.message.reply_text("📥 جاري تحميل الفيديو... انتظر ثواني")
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            await context.bot.send_video(chat_id=update.message.chat_id, video=video)
        os.remove('video.mp4')
    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ! تأكد من أن الرابط صحيح.")

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("شلونك؟ وياك بوت علي الي ينزل كلشي 🚀\n\nبس مو تنزل سوالف طايح حظها وتنزيلات مو حلوة 🗿🗿💋")

if __name__ == '__main__':
    print("✅ بوت علي جاهز للعمل!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()
    
    print("✅ البوت بدأ العمل بنجاح! جربه الآن في تلجرام.")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()
