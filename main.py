import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = 8471320360:AAHrI1iS4e4RNxs3AVUvplh1cA1pfI0XcsI

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("شلونك؟ وياك بوت علي الي ينزل كلشي 🚀\n\nبس مو تنزل سوالف طايح حظها وتنزيلات مو حلوة 🗿🗿💋")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    # جملتك الجديدة هنا
    await update.message.reply_text("جا يحمل صبر نتكم خره 🙂")
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        with open('video.mp4', 'rb') as video:
            await context.bot.send_video(chat_id=update.message.chat_id, video=video)
        os.remove('video.mp4')
    except Exception as e:
        await update.message.reply_text("❌ صار خطأ، الرابط بي مشكلة أو النت فصل.")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()
