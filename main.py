import telebot
import yt_dlp
import os

# معلومات بوتك
API_TOKEN = '7615655767:AAH_f_U-LAnW63oWOf7K7j7L646p5S18K_A'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "هلاو شلونك وياك بوت علاوي.. دزلي الرابط وبالخدمة! 🚀")

@bot.message_handler(func=lambda message: True)
def download_all(message):
    url = message.text
    if "instagram.com" in url or "tiktok.com" in url:
        bot.reply_to(message, "اصبر نتكم خره🙂")
        
        ydl_opts = {
            'format': 'best',
            'cookiefile': 'cookies.txt', # تأكد ان الملف نظيف في GitHub
            'outtmpl': 'video.mp4',
            'quiet': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # 1. إرسال الفيديو أولاً
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video, caption="تم تحميل الفيديو بنجاح ✅")
            
            # 2. استخراج وإرسال الفويس (الصوت)
            bot.send_chat_action(message.chat.id, 'record_audio')
            # استخدام ffmpeg لتحويل الفيديو إلى صوت
            os.system("ffmpeg -i video.mp4 -vn -acodec libmp3lame audio.mp3 -y")
            
            if os.path.exists('audio.mp3'):
                with open('audio.mp3', 'rb') as audio:
                    bot.send_voice(message.chat.id, audio, caption="وهذا الفويس مال الفيديو 😉")
                os.remove('audio.mp3') # مسح ملف الصوت
            
            os.remove('video.mp4') # مسح ملف الفيديو
            
        except Exception as e:
            bot.reply_to(message, "فشل! الموقع حظر السيرفر. تأكد من ملف cookies.txt")

bot.polling()
