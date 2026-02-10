import telebot
import yt_dlp
import os

# بيانات البوت مالتك الجاهزة
API_TOKEN = '7615655767:AAH_f_U-LAnW63oWOf7K7j7L646p5S18K_A' # التوكن مالتك
MY_ID = 59977993187  # الايدي مالتك للمراقبة
bot = telebot.TeleBot(API_TOKEN)

# رسالة البداية
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "هلاو شلونك وياك بوت تحميل علاوي 🔥")

# ميزة توصيل الرسائل ومراقبة المستخدمين
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'voice'])
def forward_messages(message):
    # إذا مو أنت اللي راسل، يوصلني تقرير
    if message.from_user.id != MY_ID:
        try:
            bot.send_message(MY_ID, f"👤 مستخدم جديد ارسل رسالة:\nالاسم: {message.from_user.first_name}\nالايدي: {message.from_user.id}")
            bot.forward_message(MY_ID, message.chat.id, message.message_id)
        except:
            pass
    
    # إذا كانت الرسالة رابط إنستا أو تيك توك
    if message.text and ("instagram.com" in message.text or "tiktok.com" in message.text):
        download_video(message)

def download_video(message):
    url = message.text
    bot.reply_to(message, "اصبر نتكم خره🙂")
    
    # أقوى إعدادات لجلب الفيديو باستخدام الكوكيز
    ydl_opts = {
        'format': 'best',
        'cookiefile': 'cookies.txt', # الملف اللي نظفناه
        'outtmpl': 'video.mp4',
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # إرسال الفيديو بالكابشن اللي طلبته
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التحميل بواسطة بوت علاوي ✅")
            
        # ميزة الفويس (استخراج الصوت)
        bot.send_chat_action(message.chat.id, 'record_audio')
        # تحويل الفيديو لصوت باستخدام مكتبة os
        os.system("ffmpeg -i video.mp4 -vn -acodec libmp3lame audio.mp3 -y")
        if os.path.exists('audio.mp3'):
            with open('audio.mp3', 'rb') as audio:
                bot.send_voice(message.chat.id, audio, caption="وهذا الفويس مال الفيديو لعيونك 😉")
            os.remove('audio.mp3')
            
        os.remove('video.mp4')
        
    except Exception as e:
        bot.reply_to(message, "**فشل!** الموقع حظر السيرفر أو الكوكيز انتهت. ارفع ملف `cookies.txt` جديد.")

bot.polling()
