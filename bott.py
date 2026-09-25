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

# Logging စနစ်
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Bot Token နှင့် Admin Chat ID
BOT_TOKEN = os.getenv('BOT_TOKEN', '8261373096:AAH7fjP1T1v12DiD-lyg8giVIEIxpkjSoGE')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '6146598194') # သင့် Admin ID ဂဏန်းအစစ် ပြောင်းထည့်ပါ

bot = telebot.TeleBot(BOT_TOKEN)
MM_TZ = pytz.timezone('Asia/Yangon')

# ---------------------------------------------------------
# Web Service အတွက် Fake Server (၂၄ နာရီ Run ရန်)
# ---------------------------------------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7 with Payment and 20 Tables Feature!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

keep_alive()

# ---------------------------------------------------------
# Keyboards များ (ငွေပေးချေရန် ခလုတ် ထပ်တိုးထားသည်)
# ---------------------------------------------------------
def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton('🍔 ဘာတွေရနိုင်လဲ (Menu)'),
        KeyboardButton('🎉 ပရိုမိုးရှင်း')
    )
    markup.add(
        KeyboardButton('🕒 ဆိုင်ဖွင့်ချိန်'),
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
        KeyboardButton('💳 ငွေပေးချေရန် (Payment)'),
        KeyboardButton('📝 အကြံပြုရန် / Feedback')
    )
    return markup

def cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('❌ ပယ်ဖျက်မည်'))
    return markup

# ---------------------------------------------------------
# /start & /help
# ---------------------------------------------------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    welcome_text = (
        "မင်္ဂလာပါ 🙏 **'အသဲစွဲ မိုးညို'** မှ နွေးထွေးစွာ ကြိုဆိုပါတယ်။\n\n"
        "ကျွန်တော်တို့ဆိုင်မှ အရသာရှိသော အစားအသောက်များကို အောက်ပါ Menu ခလုတ်များမှတစ်ဆင့် အလွယ်တကူ ရွေးချယ်မှာယူနိုင်ပါတယ်ခင်ဗျာ။ 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_keyboard(), parse_mode='Markdown')

# ---------------------------------------------------------
# Main Handler (ပင်မ Menu ခလုတ်များ)
# ---------------------------------------------------------
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
        current_hour = now.hour
        if 15 <= current_hour < 20:
            status_text = "🟢 **ယခုအချိန်တွင် ဆိုင်ဖွင့်ပါသည်**"
        else:
            status_text = "🔴 **ယခုအချိန်တွင် ဆိုင်ပိတ်ထားပါသည်**"
        reply_msg = f"🕒 **ဆိုင်ဖွင့်ချိန်**\nညနေ ၃:၀၀ နာရီ မှ ည ၈:၀၀ နာရီ အထိ\n🗓️ လပြည့်၊ လကွယ်နေ့များတွင် ဆိုင်ပိတ်ပါသည်။\n\nလက်ရှိအခြေအနေ: {status_text}"
        bot.send_message(chat_id, reply_msg, parse_mode='Markdown')

    elif text == '🗺️ တည်နေရာ (Location)':
        reply_msg = "📍 **ဆိုင်လိပ်စာ**\nကျွန်းရွှေဝါလမ်း၊ မြို့မရပ်ကွက်၊ မိုးညိုမြို့။\n\nဆိုင်သို့ လာရောက်ရန် အောက်ပါ Map ကို နှိပ်၍ လမ်းကြောင်းကြည့်ရှုနိုင်ပါသည်။ 👇"
        bot.send_message(chat_id, reply_msg, parse_mode='Markdown')
        bot.send_location(chat_id, latitude=17.9547, longitude=95.5342)

    elif text == '📞 ဆက်သွယ်ရန်':
        reply_msg = (
            "📞 **ဆက်သွယ်ရန် အချက်အလက်များ**\n\n"
            "📱 **ဖုန်း:** 09250597667, 09675494412\n"
            "💬 **Viber:** +959250597667\n"
            "✈️ **Telegram:** [@athaeswaemonyo](https://t.me/athaeswaemonyo)\n"
            "📘 **Facebook:** [အသဲစွဲ မိုးညို Page](https://facebook.com/)\n"
            "📸 **Instagram:** [@athaeswae_moenyo](https://instagram.com/)"
        )
        bot.send_message(chat_id, reply_msg, parse_mode='Markdown', disable_web_page_preview=True)

    # Menu အသစ်များ တိုးထားသည် (သရေစာ နှင့် ပင်လယ်စာ)
    elif text == '🍔 ဘာတွေရနိုင်လဲ (Menu)':
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🥤 အအေး မျိုးစုံ", callback_data="cat_drinks"),
            InlineKeyboardButton("🍗 ကြက်ကင်", callback_data="cat_chicken"),
            InlineKeyboardButton("🥗 အသုတ်စုံများ", callback_data="cat_salad"),
            InlineKeyboardButton("🍚 ထမင်းနှင့် ဟင်းလျာ", callback_data="cat_rice"),
            InlineKeyboardButton("🍜 ခေါက်ဆွဲ/ကြာဆံ", callback_data="cat_noodle"),
            InlineKeyboardButton("🍰 အချိုပွဲ (Dessert)", callback_data="cat_dessert"),
            InlineKeyboardButton("🍕 သရေစာ/Snacks", callback_data="cat_snacks"),
            InlineKeyboardButton("🦐 ပင်လယ်စာ", callback_data="cat_seafood")
        )
        bot.send_message(chat_id, "👇 လူကြီးမင်း ကြည့်ရှုလိုသော မီနူး အမျိုးအစားကို ရွေးချယ်ပါ-", reply_markup=markup)

    elif text == '🎉 ပရိုမိုးရှင်း':
        bot.send_chat_action(chat_id, 'upload_photo')
        img_url = "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=500&q=60"
        promo_text = (
            "🎉 **ယခုလအတွက် အထူး ပရိုမိုးရှင်းများ** 🎉\n\n"
            "🎁 **Promo 1:** ကြက်ကင် (၁) ကောင် ဝယ်ယူပါက အအေး (၁) ခွက် အခမဲ့ ရရှိပါမည်။\n"
            "🎁 **Promo 2:** စုစုပေါင်း ၅၀,၀၀၀ ကျပ်နှင့်အထက် ဝယ်ယူပါက (10% Discount) ရရှိပါမည်။\n"
            "🎁 **Promo 3:** မွေးနေ့ရှင်များအတွက် ဆိုင်သို့လာရောက်စားသုံးပါက အချိုပွဲ အခမဲ့ ဆက်သပေးပါမည် (မှတ်ပုံတင်ပြရန်)။\n\n"
            "*(ကာလ - ယခုလကုန်အထိသာ)*"
        )
        bot.send_photo(chat_id, img_url, caption=promo_text, parse_mode='Markdown')

    # Booking ပြင်ဆင်ထားသည် (ဝိုင်း ၂၀ အထိ)
    elif text == '📅 စားပွဲကြိုတင်မှာယူရန်':
        markup = InlineKeyboardMarkup(row_width=4)
        tables = []
        for i in range(1, 21): # ဝိုင်း ၂၀ အထိ ပြောင်းထားသည်
            tables.append(InlineKeyboardButton(f"ဝိုင်း {i}", callback_data=f"book_table_{i}"))
        markup.add(*tables)
        
        bot.send_message(
            chat_id, 
            "📅 **စားပွဲ (Table) Booking တင်ရန်**\n\nကျွန်တော်တို့ဆိုင်တွင် ဝိုင်း (၂၀) ရှိပါသည်။ လူကြီးမင်း ကြိုတင်ယူလိုသော ဝိုင်းနံပါတ်ကို အောက်တွင် ရွေးချယ်ပေးပါ-", 
            reply_markup=markup,
            parse_mode='Markdown'
        )

    # Delivery စာသား ပြင်ဆင်ထားသည်
    elif text == '🚚 ပို့ဆောင်မှု (Delivery)':
        reply_msg = "🚚 **ပို့ဆောင်မှု (Delivery)**\n\nတောင်းပန်အပ်ပါသည်ခင်ဗျာ။ Delivery (ပို့ဆောင်မှု) ဝန်ဆောင်မှုကို အခုရက်အတွင်းမှာ ယာယီပိတ်သိမ်းထားပါပြီ။ ဆိုင်သို့ကိုယ်တိုင်လာရောက်အားပေးရန် ဖိတ်ခေါ်အပ်ပါသည်။"
        bot.send_message(chat_id, reply_msg, parse_mode='Markdown')

    # FAQ မေးခွန်းများ တိုးထားသည် / အဖြေများ ပြင်ဆင်ထားသည်
    elif text == '❓ အမေးများသော မေးခွန်းများ (FAQ)':
        reply_msg = (
            "❓ **အမေးများသော မေးခွန်းများ**\n\n"
            "**Q: ဆိုင်မှာ ကားပါကင် ရပါသလား?**\n"
            "A: ဟုတ်ကဲ့၊ ဆိုင်ရှေ့တွင် ကား နှင့် ဆိုင်ကယ်များ လုံခြုံစွာ ရပ်နားရန် နေရာကျယ်ဝန်းစွာ ရှိပါသည်။\n\n"
            "**Q: KPay, Wave Pay ဖြင့် ရှင်းလို့ရပါသလား?**\n"
            "A: ရပါတယ်။ ငွေသားအပြင် KPay, Wave Pay ဖြင့် % အပိုပေးစရာမလိုဘဲ ရှင်းနိုင်ပါတယ်။\n\n"
            "**Q: ပါတီပွဲ / မွေးနေ့ပွဲများအတွက် နေရာငှားလို့ရလား?**\n"
            "A: ရပါပြီခင်ဗျာ။ လူ ၃၀ ကနေ ၅၀ အထိ ဆံ့တဲ့ ဆိုင်နေရာလေး ရှိပါတယ်။ ကြိုတင် Booking ပေးဖို့တော့ လိုပါမယ်။\n\n"
            "**Q: ဆိုင်မှာ Free WiFi ရပါသလား?**\n"
            "A: ဟုတ်ကဲ့၊ ဆိုင်လာစားသုံးသူတိုင်းအတွက် အခမဲ့ WiFi အသုံးပြုနိုင်အောင် စီစဥ်ပေးထားပါတယ်။\n\n"
            "**Q: အပြင်က အစားအသောက် ယူလာလို့ရပါသလား?**\n"
            "A: မွေးနေ့ကိတ်မှလွဲ၍ အခြားပြင်ပအစားအသောက်များ ယူဆောင်ခွင့် မပြုထားပါဘူးခင်ဗျာ။"
        )
        bot.send_message(chat_id, reply_msg, parse_mode='Markdown')

    # ငွေပေးချေရန် (အသစ်)
    elif text == '💳 ငွေပေးချေရန် (Payment)':
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📱 KBZ Pay", callback_data="pay_kpay"),
            InlineKeyboardButton("🌊 Wave Pay", callback_data="pay_wave"),
            InlineKeyboardButton("💼 CB Pay", callback_data="pay_cb"),
            InlineKeyboardButton("🏦 AYA Pay", callback_data="pay_aya")
        )
        bot.send_message(chat_id, "💳 **ငွေပေးချေရန်**\n\nအောက်ပါ မိမိအသုံးပြုလိုသော Mobile Banking / Wallet အမျိုးအစားကို ရွေးချယ်ပါ-", reply_markup=markup, parse_mode='Markdown')

    elif text == '📝 အကြံပြုရန် / Feedback':
        msg = bot.send_message(
            chat_id, 
            "📝 **အကြံပြုစာ ပေးပို့ရန်**\n\nဆိုင်၏ အစားအသောက်၊ ဝန်ဆောင်မှု နှင့် ပတ်သက်၍ လူကြီးမင်း၏ အကြံပြုချက်များကို ရိုက်ထည့်ပေးပို့နိုင်ပါတယ်ခင်ဗျာ။", 
            reply_markup=cancel_keyboard(),
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, process_feedback)

# ---------------------------------------------------------
# Menu Categories Callbacks (အသစ်များ အပါအဝင်)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def callback_menu_categories(call):
    chat_id = call.message.chat.id
    order_markup = InlineKeyboardMarkup()
    order_markup.add(InlineKeyboardButton("🛒 ယခုမှာယူမည် (Order Now)", callback_data="action_order"))

    if call.data == "cat_drinks":
        img_url = "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=500&q=60"
        desc = "🥤 **အအေး မျိုးစုံ**\n- ကော်ဖီ / တီး\n- သစ်သီးဖျော်ရည်များ\n- ဆိုဒါဖျော်ရည်များ"
    elif call.data == "cat_chicken":
        img_url = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=500&q=60"
        desc = "🍗 **ကြက်ကင်**\n- ပျားရည်ဆမ်း ကြက်ကင်\n- ပုံမှန် ကြက်ကင်"
    elif call.data == "cat_salad":
        img_url = "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=500&q=60"
        desc = "🥗 **အသုတ်စုံများ**\n- ခေါက်ဆွဲသုတ်\n- ပဲပြားသုတ်\n- တို့ဘူးသုပ်အမျိုးမျိုး"
    elif call.data == "cat_rice":
        img_url = "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=500&q=60"
        desc = "🍚 **ထမင်းနှင့် ဟင်းလျာ**\n- ကြက်ဆီထမင်း\n- ဝက်သားနီချက်\n- ထမင်းကြော်အမျိုးမျိုး"
    elif call.data == "cat_noodle":
        img_url = "https://images.unsplash.com/photo-1552611052-33e04de081de?auto=format&fit=crop&w=500&q=60"
        desc = "🍜 **ခေါက်ဆွဲ/ကြာဆံ**\n- ရှမ်းခေါက်ဆွဲ\n- မြေအိုးမြီးရှည်\n- ကြာဆံကြော်"
    elif call.data == "cat_dessert":
        img_url = "https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=500&q=60"
        desc = "🍰 **အချိုပွဲ**\n- ရေခဲမုန့်\n- သစ်သီးစုံပွဲ\n- ကိတ်မုန့်"
    elif call.data == "cat_snacks":
        img_url = "https://images.unsplash.com/photo-1621303837174-89787a7d4729?auto=format&fit=crop&w=500&q=60"
        desc = "🍕 **သရေစာ / Snacks**\n- အာလူးကြော်\n- ကြက်ကြော်\n- Sandwich အအေး"
    elif call.data == "cat_seafood":
        img_url = "https://images.unsplash.com/photo-1599084993091-1cb5c0721cc6?auto=format&fit=crop&w=500&q=60"
        desc = "🦐 **ပင်လယ်စာ**\n- ပုဇွန်ကင်\n- ပြည်ကြီးငါးသုပ်\n- ပင်လယ်စာအစပ်ကြော်"
    else:
        return

    bot.send_photo(chat_id, img_url, caption=desc, reply_markup=order_markup, parse_mode='Markdown')
    bot.answer_callback_query(call.id)

# ---------------------------------------------------------
# Payment Handler (ငွေပေးချေမှု နှင့် Slip တောင်းခံခြင်း)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def callback_payment(call):
    chat_id = call.message.chat.id
    pay_type = call.data.split('_')[1]
    
    # ဤနေရာတွင် မိမိဆိုင်၏ QR Code ပုံလင့်ခ်အစစ်များကို အစားထိုးနိုင်ပါသည်။
    qr_kpay = "https://cdn.phototourl.com/member/2026-09-25-000873aa-a533-48c4-9723-22ffb4bdc5ec.jpg"
    qr_wave = "https://cdn.phototourl.com/member/2026-09-25-c3c4312c-1261-46a7-9341-7a42072afeb7.jpg"
    qr_cb = "https://via.placeholder.com/400x400.png?text=CB+Pay+QR"
    qr_aya = "https://cdn.phototourl.com/member/2026-09-25-43ae1131-867f-4b6c-8662-9f264704ade3.jpg"

    if pay_type == "kpay":
        img_url = qr_kpay
        text = "📱 **KBZ Pay ဖြင့် ငွေပေးချေရန်**\n\n👤 အမည်: (သင့်အမည်)\n📞 ဖုန်း: 09250597667\n\nအထက်ပါ QR Code (သို့) ဖုန်းနံပါတ်သို့ ငွေလွှဲပြီးပါက **ငွေလွှဲပြေစာ (Screenshot)** ကို ယခု Chat Box တွင် ဓာတ်ပုံပေးပို့ပေးပါခင်ဗျာ။"
    elif pay_type == "wave":
        img_url = qr_wave
        text = "🌊 **Wave Pay ဖြင့် ငွေပေးချေရန်**\n\n👤 အမည်: (သင့်အမည်)\n📞 ဖုန်း: 09675494412\n\nအထက်ပါ QR Code (သို့) ဖုန်းနံပါတ်သို့ ငွေလွှဲပြီးပါက **ငွေလွှဲပြေစာ (Screenshot)** ကို ယခု Chat Box တွင် ဓာတ်ပုံပေးပို့ပေးပါခင်ဗျာ။"
    elif pay_type == "cb":
        img_url = qr_cb
        text = "💼 **CB Pay ဖြင့် ငွေပေးချေရန်**\n\n👤 အမည်: (သင့်အမည်)\n📞 ဖုန်း: no\n\nအထက်ပါ QR Code (သို့) ဖုန်းနံပါတ်သို့ ငွေလွှဲပြီးပါက **ငွေလွှဲပြေစာ (Screenshot)** ကို ယခု Chat Box တွင် ဓာတ်ပုံပေးပို့ပေးပါခင်ဗျာ။"
    elif pay_type == "aya":
        img_url = qr_aya
        text = "🏦 **AYA Pay ဖြင့် ငွေပေးချေရန်**\n\n👤 အမည်: (သင့်အမည်)\n📞 ဖုန်း: 09977466809\n\nအထက်ပါ QR Code (သို့) ဖုန်းနံပါတ်သို့ ငွေလွှဲပြီးပါက **ငွေလွှဲပြေစာ (Screenshot)** ကို ယခု Chat Box တွင် ဓာတ်ပုံပေးပို့ပေးပါခင်ဗျာ။"

    msg = bot.send_photo(chat_id, img_url, caption=text, reply_markup=cancel_keyboard(), parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_payment_slip, pay_type)
    bot.answer_callback_query(call.id)

def process_payment_slip(message, pay_type):
    if message.text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(message.chat.id, "ငွေပေးချေခြင်းကို ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return

    # ဓာတ်ပုံ (Slip) မဟုတ်ဘဲ စာပို့လာလျှင် ပြန်တောင်းမည်
    if not message.photo:
        msg = bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ငွေလွှဲပြေစာ (Screenshot ဓာတ်ပုံ) ကိုသာ ပို့ပေးပါ။\n(ပြန်လည်ပို့ဆောင်ရန် အောက်တွင် ပုံထည့်ပေးပါ၊ သို့မဟုတ် '❌ ပယ်ဖျက်မည်' ကိုနှိပ်ပါ)")
        bot.register_next_step_handler(msg, process_payment_slip, pay_type)
        return

    # Admin ထံသို့ Slip ပို့ပေးခြင်း
    admin_msg = (
        f"💸 **ငွေလွှဲပြေစာ အသစ် ဝင်လာပါပြီ** 💸\n\n"
        f"👤 Customer: {message.from_user.first_name}\n"
        f"💳 ပေးချေသည့်စနစ်: {pay_type.upper()}"
    )
    try:
        bot.send_message(6146598194, admin_msg, parse_mode='Markdown')
        bot.send_photo(6146598194, message.photo[-1].file_id) # ဓာတ်ပုံကို Forward လုပ်သည်
        
        bot.reply_to(message, "✅ ငွေလွှဲပြေစာ လက်ခံရရှိပါပြီ။ အော်ဒါအတွက် ကျေးဇူးအထူးတင်ရှိပါတယ်။", reply_markup=main_menu_keyboard())
    except Exception as e:
        logging.error(f"Slip Error: {e}")
        bot.reply_to(message, "⚠️ Error ဖြစ်ပေါ်နေပါသည်၊ ဖုန်းဖြင့်သာ တိုက်ရိုက် ဆက်သွယ်ပေးပါ။", reply_markup=main_menu_keyboard())


# ---------------------------------------------------------
# Table Booking Callback (ဝိုင်း ၂၀ ရွေးချယ်ခြင်း)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('book_table_'))
def callback_book_table(call):
    table_no = call.data.split('_')[2]
    msg = bot.send_message(
        call.message.chat.id, 
        f"✅ **(ဝိုင်း - {table_no})** ကို ရွေးချယ်လိုက်ပါသည်။\n\n"
        "လူကြီးမင်း၏ **အမည်၊ ဖုန်းနံပါတ်၊ လာရောက်မည့် အချိန် နှင့် လူအရေအတွက်** ကို အောက်တွင် ရိုက်ပို့ပေးပါခင်ဗျာ။\n\n"
        "*(ဥပမာ - ဦးကျော်၊ 0912345678၊ ညနေ ၅ နာရီ၊ ၄ ယောက်)*", 
        reply_markup=cancel_keyboard(),
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_booking, table_no)
    bot.answer_callback_query(call.id)

def process_booking(message, table_no):
    if message.text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(message.chat.id, "Booking တင်ခြင်းကို ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return

    admin_msg = (
        f"📅 **Booking အသစ် ဝင်လာပါပြီ** 📅\n\n"
        f"👤 Customer: {message.from_user.first_name}\n"
        f"📍 ရွေးချယ်ထားသောဝိုင်း: **ဝိုင်း {table_no}**\n"
        f"📝 အသေးစိတ်:\n{message.text}"
    )
    try:
        bot.send_message(6146598194, admin_msg, parse_mode='Markdown')
        bot.reply_to(message, f"✅ (ဝိုင်း {table_no}) အတွက် Booking တင်ခြင်း အောင်မြင်ပါသည်။ ဆိုင်မှ ပြန်လည်အတည်ပြု ဆက်သွယ်ပေးပါမည်။", reply_markup=main_menu_keyboard())
    except Exception as e:
        logging.error(f"Booking Error: {e}")
        bot.reply_to(message, "⚠️ Error ဖြစ်ပေါ်နေပါသည်၊ ဖုန်းဖြင့်သာ တိုက်ရိုက် ဆက်သွယ်ပေးပါ။", reply_markup=main_menu_keyboard())

# ---------------------------------------------------------
# Order & Feedback Processing (ယခင်အတိုင်း)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "action_order")
def callback_order(call):
    chat_id = call.message.chat.id
    msg = bot.send_message(
        chat_id, 
        "📝 **အော်ဒါတင်ရန်**\n\nမှာယူလိုသော အစားအသောက်၊ အမည်၊ ဖုန်းနံပါတ် နှင့် ပို့ဆောင်ရမည့်လိပ်စာကို ရိုက်ထည့်ပေးပါခင်ဗျာ။", 
        reply_markup=cancel_keyboard(),
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_order)
    bot.answer_callback_query(call.id)

def process_order(message):
    if message.text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(message.chat.id, "အော်ဒါတင်ခြင်းကို ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "မရှိပါ"
    admin_msg = (
        f"🛒 **အော်ဒါအသစ် ဝင်လာပါပြီ** 🛒\n\n"
        f"👤 Customer: {user.first_name}\n"
        f"🔗 Telegram: {username}\n"
        f"🆔 ID: `{user.id}`\n\n"
        f"📝 **မှာယူသည့် အချက်အလက်များ:**\n{message.text}"
    )

    admin_markup = InlineKeyboardMarkup()
    admin_markup.add(
        InlineKeyboardButton("✅ အတည်ပြု (Accept)", callback_data=f"status_accept_{user.id}"),
        InlineKeyboardButton("❌ ငြင်းပယ် (Reject)", callback_data=f"status_reject_{user.id}")
    )

    try:
        bot.send_message(6146598194, admin_msg, reply_markup=admin_markup, parse_mode='Markdown')
        bot.reply_to(message, "✅ လူကြီးမင်း၏ အော်ဒါကို လက်ခံရရှိပါပြီ။ မကြာမီ ဆိုင်မှ စစ်ဆေးအတည်ပြုပေးပါမည်။", reply_markup=main_menu_keyboard())
    except Exception as e:
        logging.error(f"Order Admin Alert Failed: {e}")
        bot.reply_to(message, "⚠️ အချက်အလက် ပို့ဆောင်ရာတွင် အဆင်မပြေဖြစ်သွားပါသည်။ ဖုန်းဖြင့် တိုက်ရိုက်ဆက်သွယ်ပေးပါ။", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith('status_'))
def handle_order_status(call):
    data = call.data.split('_')
    action = data[1]
    customer_id = data[2]

    if action == "accept":
        bot.send_message(customer_id, "🎉 **သတင်းကောင်းပါ!**\nလူကြီးမင်း၏ အော်ဒါကို ဆိုင်မှ လက်ခံလိုက်ပါပြီ။ မကြာမီ ပြင်ဆင်ပို့ဆောင်ပေးပါမည်။")
        bot.edit_message_text(f"{call.message.text}\n\n🟢 **[Status: အော်ဒါလက်ခံပြီး]**", call.message.chat.id, call.message.message_id)
    elif action == "reject":
        bot.send_message(customer_id, "⚠️ **တောင်းပန်အပ်ပါသည်**\nလူကြီးမင်း၏ အော်ဒါမှာ ပစ္စည်းကုန်သွားခြင်း (သို့) ဆိုင်ပိတ်သွားခြင်းကြောင့် လက်မခံနိုင်တော့ပါခင်ဗျာ။")
        bot.edit_message_text(f"{call.message.text}\n\n🔴 **[Status: ပယ်ဖျက်လိုက်သည်]**", call.message.chat.id, call.message.message_id)

    bot.answer_callback_query(call.id)

def process_feedback(message):
    if message.text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(message.chat.id, "အကြံပြုချက် ပေးပို့ခြင်းကို ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return

    admin_msg = (
        f"📝 **Feedback ဝင်လာပါပြီ** 📝\n\n"
        f"👤 မှတ်ချက်ပေးသူ: {message.from_user.first_name}\n"
        f"🆔 ID: `{message.from_user.id}`\n"
        f"💬 အကြံပြုချက်:\n{message.text}"
    )
    try:
        bot.send_message(6146598194, admin_msg, parse_mode='Markdown')
        bot.reply_to(message, "💖 အဖိုးတန်လှသော အကြံပြုချက်အတွက် ကျေးဇူးအထူးတင်ရှိပါတယ်။ ပိုမိုကောင်းမွန်အောင် ကြိုးစားသွားပါမည်။", reply_markup=main_menu_keyboard())
    except Exception as e:
        logging.error(f"Feedback Error: {e}")
        bot.reply_to(message, "⚠️ Error ဖြစ်ပေါ်နေပါသည်။", reply_markup=main_menu_keyboard())

# ---------------------------------------------------------
# စတင် run ခြင်း
# ---------------------------------------------------------
if __name__ == '__main__':
    print("အသဲစွဲမိုးညို Ultra Pro Bot စတင် အလုပ်လုပ်နေပါပြီ...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
