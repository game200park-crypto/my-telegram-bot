import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# 1. ضع توكن البوت الخاص بك من BotFather بين العلامتين
BOT_TOKEN = "8276214359:AAH1Nzyspy0cs70l9s9RkbCg6CHuGne_kFw"
# 2. ضع معرف قناتك (يجب أن يبدأ بـ @ وأن يكون البوت مشرفاً فيها)
CHANNEL_USERNAME = "@zonehd7111" 
# 3. الـ File ID الخاص بالفيديو الذي استخرجته للتو
VIDEO_FILE_ID = "BAACAgIAAxkBAAEtkPxqf1-D_R2zx86aHLR3IBvpN7ROuAACTq0AAtMD-EuCLf9QED8eXD0E"
bot = telebot.TeleBot(BOT_TOKEN)
# دالة الفحص هل المستخدم مشترك بالقناة؟
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['creator', 'administrator', 'member']
    except Exception as e:
        print(f"Error: {e}")
        return False
# إنشاء أزرار الاشتراك
def get_keyboard():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("📢 اشترك في القناة أولاً", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")
    btn2 = InlineKeyboardButton("✅ تحقّق من الاشتراك", callback_data="check")
    markup.add(btn1)
    markup.add(btn2)
    return markup
# عند الضغط على /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        bot.reply_to(message, "👋 أهلاً بك! أنت مشترك بالفعل بالقناة.\n\nأرسل /video للحصول على الفيديو.")
    else:
        bot.send_message(
            message.chat.id,
            "⚠️ **عذراً! يجب عليك الاشتراك في القناة أولاً لاستخدام البوت.**\n\nاشترك ثم اضغط على زر التحقق أدناه:",
            parse_mode="Markdown",
            reply_markup=get_keyboard()
        )
# عند الضغط على زر "تحقق من الاشتراك"
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق، شكراً لاشتراكك!")
        bot.send_message(call.message.chat.id, "🎉 يمكنك الآن إرسال /video للحصول على الفيديو.")
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك في القناة بعد!", show_alert=True)
# عند طلب الفيديو /video
@bot.message_handler(commands=['video'])
def send_vid(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "⚠️ يجب أن تشترك بالقناة أولاً!", reply_markup=get_keyboard())
        return
    bot.send_message(message.chat.id, "⏳ جاري إرسال الفيديو...")
    bot.send_video(message.chat.id, VIDEO_FILE_ID, caption="🎬 تفضل الفيديو الخاص بك!")
print("البوت يعمل...")
bot.infinity_polling()
