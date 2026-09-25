import os
import time
import logging
import threading
from datetime import datetime
import pytz
import telebot
from telebot.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from flask import Flask

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# =====================================================================
# နေရာ (၁) - သင့် BOT TOKEN နှင့် ADMIN ID ထည့်ရန် နေရာ
# =====================================================================
BOT_TOKEN = os.getenv('BOT_TOKEN', '8261373096:AAH7fjP1T1v12DiD-lyg8giVIEIxpkjSoGE') # ဥပမာ - '8261373096:AAH...'
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '6146598194') # ဥပမာ - '123456789'

bot = telebot.TeleBot(BOT_TOKEN)
MM_TZ = pytz.timezone('Asia/Yangon')

app = Flask('')
@app.route('/')
def home():
    return "Bot is running 24/7 with Payment Features!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = threading.Thread(target=run)
    t.start()
keep_alive()

def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton('🍔 ဘာတွေရနိုင်လဲ (Menu)'),
        KeyboardButton('💳 ငွေပေးချေရန် (Payment)') # ပေးချေရန် ခလုတ်အသစ်
    )
    markup.add(
        KeyboardButton('🎉 ပရိုမိုးရှင်း'),
        KeyboardButton('📅 စားပွဲကြိုတင်မှာယူရန်')
    )
    markup.add(
        KeyboardButton('🗺️ တည်နေရာ (Location)'),
        KeyboardButton('📞 ဆက်သွယ်ရန်')
    )
    markup.add(
        KeyboardButton('🚚 ပို့ဆောင်မှု (Delivery)'),
        KeyboardButton('❓ အမေးများသော မေးခွန်းများ (FAQ)')
    )
    markup.add(
        KeyboardButton('📝 အကြံပြုရန် / Feedback')
    )
    return markup

def cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('❌ ပယ်ဖျက်မည်'))
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    welcome_text = "မင်္ဂလာပါ 🙏 **'အသဲစွဲ မိုးညို'** မှ နွေးထွေးစွာ ကြိုဆိုပါတယ်။\n\nအောက်ပါ Menu ခလုတ်များမှတစ်ဆင့် ဝန်ဆောင်မှုများကို အသုံးပြုနိုင်ပါတယ်ခင်ဗျာ။ 👇"
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_keyboard(), parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    chat_id = message.chat.id

    if text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(chat_id, "အဓိက မီနူးသို့ ပြန်ရောက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return

    bot.send_chat_action(chat_id, 'typing')
    time.sleep(0.3)

    if text == '🕒 ဆိုင်ဖွင့်ချိန်':
        now = datetime.now(MM_TZ)
        status_text = "🟢 **ယခုအချိန်တွင် ဆိုင်ဖွင့်ပါသည်**" if 15 <= now.hour < 20 else "🔴 **ယခုအချိန်တွင် ဆိုင်ပိတ်ထားပါသည်**"
        bot.send_message(chat_id, f"🕒 **ဆိုင်ဖွင့်ချိန်**\nညနေ ၃:၀၀ နာရီ မှ ည ၈:၀၀ နာရီ အထိ\nလက်ရှိအခြေအနေ: {status_text}", parse_mode='Markdown')

    elif text == '🗺️ တည်နေရာ (Location)':
        bot.send_message(chat_id, "📍 **ဆိုင်လိပ်စာ**\nကျွန်းရွှေဝါလမ်း၊ မြို့မရပ်ကွက်၊ မိုးညိုမြို့။ 👇", parse_mode='Markdown')
        bot.send_location(chat_id, latitude=17.9547, longitude=95.5342)

    elif text == '📞 ဆက်သွယ်ရန်':
        bot.send_message(chat_id, "📞 **ဆက်သွယ်ရန်**\n📱 ဖုန်း: 09250597667\n✈️ Telegram: @athaeswaemonyo", parse_mode='Markdown')

    elif text == '🍔 ဘာတွေရနိုင်လဲ (Menu)':
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🥤 အအေး", callback_data="cat_drinks"),
            InlineKeyboardButton("🍗 ကြက်ကင်", callback_data="cat_chicken"),
            InlineKeyboardButton("🥗 အသုတ်စုံ", callback_data="cat_salad"),
            InlineKeyboardButton("🦐 ပင်လယ်စာ (New)", callback_data="cat_seafood") # Menu အသစ်
        )
        bot.send_message(chat_id, "👇 ကြည့်ရှုလိုသော မီနူး အမျိုးအစားကို ရွေးချယ်ပါ-", reply_markup=markup)

    elif text == '🎉 ပရိုမိုးရှင်း':
        bot.send_message(chat_id, "🎉 **ပရိုမိုးရှင်း**\nကြက်ကင် (၁) ကောင် ဝယ်ယူပါက အအေး (၁) ခွက် အခမဲ့ ရရှိပါမည်။", parse_mode='Markdown')

    elif text == '📅 စားပွဲကြိုတင်မှာယူရန်':
        markup = InlineKeyboardMarkup(row_width=5) # ၅ ခု တစ်တန်းစီ
        tables = [InlineKeyboardButton(f"{i}", callback_data=f"book_table_{i}") for i in range(1, 21)] # ဝိုင်း ၂၀
        markup.add(*tables)
        bot.send_message(chat_id, "📅 **စားပွဲ Booking (ဝိုင်း ၁ မှ ၂၀ အထိ)**\nလူကြီးမင်း ကြိုတင်ယူလိုသော ဝိုင်းနံပါတ်ကို ရွေးချယ်ပါ-", reply_markup=markup, parse_mode='Markdown')

    elif text == '🚚 ပို့ဆောင်မှု (Delivery)':
        bot.send_message(chat_id, "🚚 **Delivery ဝန်ဆောင်မှု**\n\nတောင်းပန်အပ်ပါသည်ခင်ဗျာ။ ယခုရက်ပိုင်းအတွင်း ပို့ဆောင်မှု (Delivery) ဝန်ဆောင်မှုကို ယာယီ ပိတ်သိမ်းထားပါသည်။", parse_mode='Markdown')

    elif text == '❓ အမေးများသော မေးခွန်းများ (FAQ)':
        faq = (
            "❓ **အမေးများသော မေးခွန်းများ**\n\n"
            "**Q: ပါတီပွဲ / မွေးနေ့ပွဲများအတွက် နေရာငှားလို့ရလား?**\n"
            "A: ရပါပြီ ခင်ဗျာ။ လူ ၃၀ ကနေ ၅၀ အထိ ဆံ့တဲ့ ဆိုင်နေရာ၊ စားပွဲဝိုင်းတွေ ရှိပါတယ်။ ကြိုတင် Booking တော့ ပေးဖို့လိုပါတယ်ခင်ဗျာ။\n\n"
            "**Q: KPay, Wave Pay ဖြင့် ရှင်းလို့ရပါသလား?**\n"
            "A: ရပါတယ်။ % အပိုပေးစရာမလိုဘဲ ငွေပေးချေရန် Menu မှတဆင့် ရှင်းနိုင်ပါတယ်။\n\n"
            "**Q: ကားပါကင် အဆင်ပြေလား?**\n"
            "A: ဆိုင်ရှေ့တွင် ကား/ဆိုင်ကယ် ရပ်နားရန် နေရာကျယ်ဝန်းစွာ ရှိပါသည်။"
        )
        bot.send_message(chat_id, faq, parse_mode='Markdown')

    elif text == '💳 ငွေပေးချေရန် (Payment)':
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📲 KPay", callback_data="pay_kpay"),
            InlineKeyboardButton("🌊 WavePay", callback_data="pay_wave"),
            InlineKeyboardButton("🏦 CB Pay", callback_data="pay_cb"),
            InlineKeyboardButton("🅰️ AYA Pay", callback_data="pay_aya")
        )
        bot.send_message(chat_id, "💳 **ငွေပေးချေရန် (Payment)**\n\nအောက်ပါ ဘဏ်အကောင့်များမှတဆင့် ငွေပေးချေနိုင်ပါသည်။ အသုံးပြုမည့် Pay ကို ရွေးချယ်ပါ-", reply_markup=markup, parse_mode='Markdown')

    elif text == '📝 အကြံပြုရန် / Feedback':
        msg = bot.send_message(chat_id, "📝 အကြံပြုချက်များကို ရိုက်ထည့်ပေးပို့နိုင်ပါတယ်ခင်ဗျာ။", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(msg, process_feedback)

# ---------------------------------------------------------
# PAYMENT & SLIP UPLOAD (ငွေပေးချေမှု နှင့် ပြေစာပေးပို့ခြင်း)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def handle_payment_methods(call):
    chat_id = call.message.chat.id
    method = call.data.split('_')[1]

    # =====================================================================
    # နေရာ (၂) - သင့် Pay ဖုန်းနံပါတ် နှင့် QR Code ပုံ (Link) ထည့်ရန် နေရာများ
    # =====================================================================
    if method == "kpay":
        phone_no = "09250597667 (yee yee cho)"
        qr_img_url = "https://cdn.phototourl.com/member/2026-09-25-000873aa-a533-48c4-9723-22ffb4bdc5ec.jpg" # <--- Kpay QR ပုံ Link ကို ဒီမှာထည့်ပါ
        
    elif method == "wave":
        phone_no = "09675494412 (yee yee cho)"
        qr_img_url = "https://cdn.phototourl.com/member/2026-09-25-c3c4312c-1261-46a7-9341-7a42072afeb7.jpg" # <--- Wave QR ပုံ Link ကို ဒီမှာထည့်ပါ
        
    elif method == "cb":
        phone_no = "0000-1111-2222-3333 (CB Pay)"
        qr_img_url = "https://example.com/your_cb_qr.jpg" # <--- CB QR ပုံ Link ကို ဒီမှာထည့်ပါ
        
    elif method == "aya":
        phone_no = "09977466809 (pyaephyoaung)"
        qr_img_url = "https://cdn.phototourl.com/member/2026-09-25-43ae1131-867f-4b6c-8662-9f264704ade3.jpg" # <--- AYA QR ပုံ Link ကို ဒီမှာထည့်ပါ

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📸 ငွေလွှဲပြေစာ (Slip) ပို့ရန်", callback_data="action_send_slip"))
    
    pay_text = f"💳 **ငွေပေးချေရန် အချက်အလက်**\n\nအောက်ပါဖုန်းနံပါတ် သို့မဟုတ် QR Code သို့ ငွေလွှဲနိုင်ပါသည်။\n📱 **ဖုန်းနံပါတ်:** `{phone_no}`\n\nငွေလွှဲပြီးပါက အောက်ပါ 'ပြေစာ (Slip) ပို့ရန်' ခလုတ်ကိုနှိပ်ပါ။"
    bot.send_photo(chat_id, qr_img_url, caption=pay_text, reply_markup=markup, parse_mode='Markdown')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "action_send_slip")
def ask_for_slip(call):
    chat_id = call.message.chat.id
    msg = bot.send_message(chat_id, "📤 ကျေးဇူးပြု၍ ငွေလွှဲထားသော **Screenshot ပြေစာ (Slip) ဓာတ်ပုံ** ကို ယခု Chat တွင် ပို့ပေးပါခင်ဗျာ။", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, receive_slip)
    bot.answer_callback_query(call.id)

def receive_slip(message):
    if message.text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(message.chat.id, "ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return

    if message.content_type == 'photo':
        user = message.from_user
        slip_caption = f"💸 **ငွေလွှဲပြေစာ အသစ် ဝင်လာပါပြီ** 💸\n👤 ပေးပို့သူ: {user.first_name}\n🆔 ID: `{user.id}`"
        try:
            bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=slip_caption, parse_mode='Markdown')
            bot.reply_to(message, "✅ ပြေစာ လက်ခံရရှိပါပြီ။ ငွေဝင်/မဝင် စစ်ဆေးပြီးပါက အကြောင်းပြန်ပေးပါမည်။ ကျေးဇူးတင်ပါတယ်။", reply_markup=main_menu_keyboard())
        except Exception as e:
            bot.reply_to(message, "⚠️ Admin ထံ ပို့ဆောင်ရာတွင် အဆင်မပြေဖြစ်သွားပါသည်။")
    else:
        msg = bot.send_message(message.chat.id, "⚠️ ကျေးဇူးပြု၍ ပြေစာကို **ဓာတ်ပုံ (Photo)** အနေဖြင့်သာ ပေးပို့ပေးပါခင်ဗျာ။", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(msg, receive_slip)

# ---------------------------------------------------------
# Menu Categories (မီနူး အသစ်များ)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def callback_menu_categories(call):
    chat_id = call.message.chat.id
    order_markup = InlineKeyboardMarkup()
    order_markup.add(InlineKeyboardButton("🛒 ယခုမှာယူမည် (Order Now)", callback_data="action_order"))

    if call.data == "cat_drinks":
        img_url = "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500"
        desc = "🥤 **အအေး မျိုးစုံ**"
    elif call.data == "cat_seafood": # မီနူးအသစ်
        img_url = "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=500"
        desc = "🦐 **ပင်လယ်စာ အထူးဟင်းလျာများ**\n- ပုစွန်ကင်\n- ပြည်ကြီးငါးသုပ်\n- ဂဏန်းမဆလာ"
    else:
        img_url = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?w=500"
        desc = "🍗 **အရသာရှိသော ဟင်းလျာများ**"

    bot.send_photo(chat_id, img_url, caption=desc, reply_markup=order_markup, parse_mode='Markdown')
    bot.answer_callback_query(call.id)

# ---------------------------------------------------------
# Table Booking (ဝိုင်း ၁ မှ ၂၀)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('book_table_'))
def callback_book_table(call):
    table_no = call.data.split('_')[2]
    msg = bot.send_message(
        call.message.chat.id, 
        f"✅ **(ဝိုင်း နံပါတ် - {table_no})** ကို ရွေးချယ်လိုက်ပါသည်။\nအမည်၊ ဖုန်း၊ အချိန် နှင့် လူအရေအတွက် ရိုက်ပို့ပေးပါ။", 
        reply_markup=cancel_keyboard()
    )
    bot.register_next_step_handler(msg, process_booking, table_no)
    bot.answer_callback_query(call.id)

def process_booking(message, table_no):
    if message.text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(message.chat.id, "ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return
    admin_msg = f"📅 **Booking အသစ်**\n👤 {message.from_user.first_name}\n📍 **ဝိုင်း {table_no}**\n📝 {message.text}"
    bot.send_message(ADMIN_CHAT_ID, admin_msg, parse_mode='Markdown')
    bot.reply_to(message, f"✅ (ဝိုင်း {table_no}) Booking အောင်မြင်ပါသည်။", reply_markup=main_menu_keyboard())

# ---------------------------------------------------------
# အော်ဒါတင်ခြင်း နှင့် Feedback (မူလအတိုင်း လုံးဝမပြောင်းပါ)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "action_order")
def callback_order(call):
    msg = bot.send_message(call.message.chat.id, "📝 မှာယူလိုသော အစားအသောက်၊ အမည်၊ ဖုန်း နှင့် လိပ်စာကို ရိုက်ထည့်ပေးပါ။", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, process_order)
    bot.answer_callback_query(call.id)

def process_order(message):
    if message.text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(message.chat.id, "ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return
    user = message.from_user
    admin_msg = f"🛒 **အော်ဒါအသစ်**\n👤 {user.first_name}\n📝 {message.text}"
    admin_markup = InlineKeyboardMarkup()
    admin_markup.add(
        InlineKeyboardButton("✅ အတည်ပြု", callback_data=f"status_accept_{user.id}"),
        InlineKeyboardButton("❌ ငြင်းပယ်", callback_data=f"status_reject_{user.id}")
    )
    bot.send_message(ADMIN_CHAT_ID, admin_msg, reply_markup=admin_markup, parse_mode='Markdown')
    bot.reply_to(message, "✅ အော်ဒါ လက်ခံရရှိပါပြီ။", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith('status_'))
def handle_order_status(call):
    data = call.data.split('_')
    action, customer_id = data[1], data[2]
    if action == "accept":
        bot.send_message(customer_id, "🎉 အော်ဒါ လက်ခံလိုက်ပါပြီ။")
    elif action == "reject":
        bot.send_message(customer_id, "⚠️ တောင်းပန်အပ်ပါသည်၊ အော်ဒါ လက်မခံနိုင်တော့ပါ။")
    bot.answer_callback_query(call.id)

def process_feedback(message):
    if message.text == '❌ ပယ်ဖျက်မည်':
        return bot.send_message(message.chat.id, "ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
    bot.send_message(ADMIN_CHAT_ID, f"📝 **Feedback**\n👤 {message.from_user.first_name}\n💬 {message.text}", parse_mode='Markdown')
    bot.reply_to(message, "💖 အကြံပြုချက်အတွက် ကျေးဇူးတင်ပါတယ်။", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    print("Bot 24/7 Started with Payment Features...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
