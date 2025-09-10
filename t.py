import telebot
from telebot import types

# ---------------- الإعدادات ----------------
API_TOKEN = '8282235189:AAF_-thF7yIDQihNdMOREJqIvpxYjbAK730'
ADMIN_ID = 2075630383  # آيدي المدير
bot = telebot.TeleBot(API_TOKEN)

# ---------------- بيانات البوت ----------------
user_data = {}

# ---------------- لوحة الأوامر ----------------
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📋 القائمة الرئيسية')
    if chat_id == ADMIN_ID:
        markup.row('🛠 لوحة الادمن')
    bot.send_message(chat_id, "مرحباً! اختر أمر:", reply_markup=markup)

# ---------------- القائمة الرئيسية ----------------
@bot.message_handler(func=lambda message: message.text == '📋 القائمة الرئيسية')
def main_menu(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🖼 إرسال صورة', '📄 إرسال نص')
    if chat_id == ADMIN_ID:
        markup.row('🛠 لوحة الادمن')
    bot.send_message(chat_id, "اختر الخيار:", reply_markup=markup)

# ---------------- لوحة الادمن ----------------
@bot.message_handler(func=lambda message: message.text == '🛠 لوحة الادمن')
def admin_panel(message):
    chat_id = message.chat.id
    if chat_id != ADMIN_ID:
        bot.send_message(chat_id, "❌ أنت لست الادمن!")
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📢 إرسال رسالة للجميع', '📝 عرض البيانات')
    markup.row('⚙️ إعدادات البوت', '⬅️ العودة للقائمة الرئيسية')
    bot.send_message(chat_id, "لوحة الادمن:", reply_markup=markup)

# ---------------- أوامر الادمن ----------------
@bot.message_handler(func=lambda message: message.text == '📢 إرسال رسالة للجميع')
def broadcast(message):
    chat_id = message.chat.id
    if chat_id != ADMIN_ID:
        return
    msg = bot.send_message(chat_id, "اكتب الرسالة التي تريد ارسالها للجميع:")
    bot.register_next_step_handler(msg, send_to_all)

def send_to_all(message):
    text = message.text
    # هنا ممكن تخزن معرفات المستخدمين مسبقاً
    user_ids = [123456789, 987654321]  # ضع آيدي المستخدمين هنا
    for uid in user_ids:
        try:
            bot.send_message(uid, f"📢 رسالة من الادمن:\n\n{text}")
        except:
            continue
    bot.send_message(ADMIN_ID, "تم الإرسال!")

@bot.message_handler(func=lambda message: message.text == '📝 عرض البيانات')
def view_data(message):
    if message.chat.id != ADMIN_ID:
        return
    bot.send_message(ADMIN_ID, f"البيانات المخزنة: {user_data}")

@bot.message_handler(func=lambda message: message.text == '⚙️ إعدادات البوت')
def bot_settings(message):
    if message.chat.id != ADMIN_ID:
        return
    bot.send_message(ADMIN_ID, "⚙️ هنا يمكن وضع إعدادات البوت")

@bot.message_handler(func=lambda message: message.text == '⬅️ العودة للقائمة الرئيسية')
def back_to_main(message):
    main_menu(message)

# ---------------- تشغيل البوت ----------------
bot.infinity_polling()