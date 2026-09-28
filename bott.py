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
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '6146598194') # သင့် ID ဂဏန်းအစစ် ပြောင်းထည့်ပါ

bot = telebot.TeleBot(BOT_TOKEN)
MM_TZ = pytz.timezone('Asia/Yangon')

# ---------------------------------------------------------
# Web Service အတွက် Fake Server (၂၄ နာရီ Run ရန်)
# ---------------------------------------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7 with Fast Text Menus & Fixed Booking!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

keep_alive()

# ---------------------------------------------------------
# Keyboards များ 
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
        KeyboardButton('💳 ငွေပေးချေရန်'),
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

    elif text == '🍔 ဘာတွေရနိုင်လဲ (Menu)':
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🥤 အအေး မျိုးစုံ", callback_data="cat_drinks"),
            InlineKeyboardButton("🍗 ကြက်ကင်", callback_data="cat_chicken"),
            InlineKeyboardButton("🥗 အသုတ်စုံများ", callback_data="cat_salad"),
            InlineKeyboardButton("🍚 ထမင်းနှင့် ဟင်းလျာ", callback_data="cat_rice"),
            InlineKeyboardButton("🍜 ခေါက်ဆွဲ/ကြာဆံ", callback_data="cat_noodle"),
            InlineKeyboardButton("🍰 အချိုပွဲ (Dessert)", callback_data="cat_dessert")
        )
        bot.send_message(chat_id, "👇 လူကြီးမင်း ကြည့်ရှုလိုသော မီနူး အမျိုးအစားကို ရွေးချယ်ပါ-", reply_markup=markup)

    elif text == '🎉 ပရိုမိုးရှင်း':
        bot.send_chat_action(chat_id, 'typing')
        promo_text = (
            "🎉 **ယခုလအတွက် အထူး ပရိုမိုးရှင်းများ** 🎉\n\n"
            "🎁 **Promo 1:** ကြက်ကင် (၁) ကောင် ဝယ်ယူပါက အအေး (၁) ခွက် အခမဲ့ ရရှိပါမည်။\n"
            "🎁 **Promo 2:** စုစုပေါင်း ၅၀,၀၀၀ ကျပ်နှင့်အထက် ဝယ်ယူပါက (10% Discount) ရရှိပါမည်။\n"
            "🎁 **Promo 3:** မွေးနေ့ရှင်များအတွက် ဆိုင်သို့လာရောက်စားသုံးပါက အချိုပွဲ အခမဲ့ ဆက်သပေးပါမည် (မှတ်ပုံတင်ပြရန်)။\n\n"
            "*(ကာလ - ယခုလကုန်အထိသာ)*"
        )
        bot.send_message(chat_id, promo_text, parse_mode='Markdown')

    elif text == '📅 စားပွဲကြိုတင်မှာယူရန်':
        markup = InlineKeyboardMarkup(row_width=4)
        tables = [InlineKeyboardButton(f"စားပွဲ {i}", callback_data=f"book_table_{i}") for i in range(1, 21)]
        markup.add(*tables)
        
        bot.send_message(
            chat_id, 
            "📅 **စားပွဲ (Table) Booking တင်ရန်**\n\nကျွန်တော်တို့ဆိုင်တွင် စားပွဲဝိုင်းပေါင်း (၂၀) ရှိပါသည်။ လူကြီးမင်း ကြိုတင်ယူလိုသော စားပွဲနံပါတ်ကို အောက်တွင် ရွေးချယ်ပေးပါ-", 
            reply_markup=markup,
            parse_mode='Markdown'
        )

    elif text == '🚚 ပို့ဆောင်မှု (Delivery)':
        reply_msg = (
            "🚚 **Delivery ဝန်ဆောင်မှု အချက်အလက်များ**\n\n"
            "တောင်းပန်အပ်ပါသည်ခင်ဗျာ။ ပို့ဆောင်မှု (Delivery) ဝန်ဆောင်မှုကို အခုရက်အတွင်းမှာ **ပိတ်သိမ်းထားပါသည်**။\n\nဆိုင်သို့ကိုယ်တိုင်လာရောက်၍သော်လည်းကောင်း၊ ပါဆယ်လာရောက်ဝယ်ယူ၍သော်လည်းကောင်း အားပေးနိုင်ပါသည်ခင်ဗျာ။"
        )
        bot.send_message(chat_id, reply_msg, parse_mode='Markdown')

    elif text == '❓ အမေးများသော မေးခွန်းများ (FAQ)':
        reply_msg = (
            "❓ **အမေးများသော မေးခွန်းများ**\n\n"
            "**Q: ပါတီပွဲ / မွေးနေ့ပွဲများအတွက် နေရာငှားလို့ရလား?**\n"
            "A: ရပါပြီခင်ဗျာ။ လူ ၃၀ ကနေ ၅၀ အထိ ဆံ့တဲ့ စားပွဲ/နေရာတွေ ရှိပါတယ်။ ကြိုတင် Booking ပေးဖို့တော့ လိုပါတယ်ခင်ဗျာ။\n\n"
            "**Q: ဆိုင်မှာ ကားပါကင် ရပါသလား?**\n"
            "A: ဟုတ်ကဲ့၊ ဆိုင်ရှေ့တွင် ကား နှင့် ဆိုင်ကယ်များ လုံခြုံစွာ ရပ်နားရန် နေရာကျယ်ဝန်းစွာ ရှိပါသည်။\n\n"
            "**Q: အသတ်သက်လွတ် သီးသန့်ရနိုင်မလား?**\n"
            "A: ရပါတယ်ခင်ဗျာ၊ သီးသန့်မှာယူနိုင်ပါတယ်။\n\n"
            "**Q: အိမ်မွေးတိရစ္ဆာန် ခေါ်လာလို့ရလား?**\n"
            "A: အခြားစားသုံးသူများ အဆင်ပြေစေရန် အိမ်မွေးတိရစ္ဆာန် ခေါ်ဆောင်လာခြင်းကို ခွင့်မပြုထားပါဘူးခင်ဗျာ။"
        )
        bot.send_message(chat_id, reply_msg, parse_mode='Markdown')

    elif text == '💳 ငွေပေးချေရန်':
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔹 KBZPay (KPay)", callback_data="pay_kpay"),
            InlineKeyboardButton("🌊 WavePay", callback_data="pay_wave"),
            InlineKeyboardButton("🏦 CB Pay", callback_data="pay_cb"),
            InlineKeyboardButton("🔴 AYA Pay", callback_data="pay_aya")
        )
        bot.send_message(
            chat_id, 
            "💳 **ငွေပေးချေရန် (Payment Options)**\n\nအောက်ပါ ငွေပေးချေမှုစနစ်များမှတစ်ဆင့် ရှင်းလင်းနိုင်ပါသည်။ လူကြီးမင်း အသုံးပြုမည့် ဘဏ်အမျိုးအစားကို ရွေးချယ်ပါ-", 
            reply_markup=markup, 
            parse_mode='Markdown'
        )

    elif text == '📝 အကြံပြုရန် / Feedback':
        msg = bot.send_message(
            chat_id, 
            "📝 **အကြံပြုစာ ပေးပို့ရန်**\n\nဆိုင်၏ အစားအသောက်၊ ဝန်ဆောင်မှု နှင့် ပတ်သက်၍ လူကြီးမင်း၏ အကြံပြုချက်များကို ရိုက်ထည့်ပေးပို့နိုင်ပါတယ်ခင်ဗျာ။", 
            reply_markup=cancel_keyboard(),
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, process_feedback)

# ---------------------------------------------------------
# Payment Callbacks (ပုံမသုံးတော့ပါ - စာသားသီးသန့်)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def callback_payment(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    method = call.data.split('_')[1]
    
    slip_markup = InlineKeyboardMarkup()
    slip_markup.add(InlineKeyboardButton("🧾 ငွေလွှဲပြေစာ (Slip) ပို့ရန်", callback_data="action_send_slip"))

    if method == "kpay":
        desc = "💳 **KBZPay (KPay) ဖြင့်ပေးချေရန်**\n\n👤 အမည်: YEE YEE CHO\n📱 ဖုန်း: `09250597667` (နှိပ်၍ Copy ကူးပါ)\n\nအထက်ပါ ဖုန်းနံပါတ်သို့ ငွေလွှဲပေးချေနိုင်ပါသည်။ ပြီးပါက အောက်ပါ 'ငွေလွှဲပြေစာ ပို့ရန်' ခလုတ်ကိုနှိပ်၍ Slip ပြန်ပို့ပေးပါခင်ဗျာ။"
    elif method == "wave":
        desc = "🌊 **WavePay ဖြင့်ပေးချေရန်**\n\n👤 အမည်: YEE YEE CHO\n📱 ဖုန်း: `09675494412`\n\nအထက်ပါ ဖုန်းနံပါတ်သို့ ငွေလွှဲပေးချေနိုင်ပါသည်။ ပြီးပါက အောက်ပါ 'ငွေလွှဲပြေစာ ပို့ရန်' ခလုတ်ကိုနှိပ်၍ Slip ပြန်ပို့ပေးပါခင်ဗျာ။"
    elif method == "cb":
        desc = "🏦 **CB Pay ဖြင့်ပေးချေရန်**\n\n👤 အမည်: YEE YEE CHO\n📱 ဖုန်း: `NO`\n\nအထက်ပါ ဖုန်းနံပါတ်သို့ ငွေလွှဲပေးချေနိုင်ပါသည်။ ပြီးပါက အောက်ပါ 'ငွေလွှဲပြေစာ ပို့ရန်' ခလုတ်ကိုနှိပ်၍ Slip ပြန်ပို့ပေးပါခင်ဗျာ။"
    elif method == "aya":
        desc = "🔴 **AYA Pay ဖြင့်ပေးချေရန်**\n\n👤 အမည်: PYAE PHYO AUNG\n📱 ဖုန်း: `09977466809`\n\nအထက်ပါ ဖုန်းနံပါတ်သို့ ငွေလွှဲပေးချေနိုင်ပါသည်။ ပြီးပါက အောက်ပါ 'ငွေလွှဲပြေစာ ပို့ရန်' ခလုတ်ကိုနှိပ်၍ Slip ပြန်ပို့ပေးပါခင်ဗျာ။"
    else:
        return

    # ပုံမပို့တော့ဘဲ Message အဖြစ်သာ ချက်ချင်းပို့ပေးမည်
    bot.send_message(chat_id, desc, reply_markup=slip_markup, parse_mode='Markdown')

# ---------------------------------------------------------
# Slip ပေးပို့ခြင်း အပိုင်း
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "action_send_slip")
def callback_send_slip(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    msg = bot.send_message(
        chat_id, 
        "🧾 **ငွေလွှဲပြေစာ ပေးပို့ရန်**\n\nလူကြီးမင်း ငွေလွှဲထားသော Screenshot (Slip) ဓာတ်ပုံကို ယခု Chat Box သို့ တိုက်ရိုက် ပေးပို့ပေးပါခင်ဗျာ။", 
        reply_markup=cancel_keyboard(), 
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_slip_upload)

def process_slip_upload(message):
    if message.text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(message.chat.id, "ငွေလွှဲပြေစာ ပေးပို့ခြင်းကို ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return

    if message.photo:
        admin_msg = (
            f"🧾 **ငွေလွှဲပြေစာ (Slip) အသစ် ဝင်လာပါပြီ**\n\n"
            f"👤 Customer: {message.from_user.first_name}\n"
            f"🆔 ID: `{message.from_user.id}`"
        )
        try:
            bot.send_message(6146598194, admin_msg, parse_mode='Markdown')
            bot.forward_message(6146598194, message.chat.id, message.message_id)
            bot.reply_to(message, "✅ ငွေလွှဲပြေစာ လက်ခံရရှိပါပြီ။ ဆိုင်မှ အတည်ပြုပြီးပါက အော်ဒါစီစဥ်ပေးပါမည်။ ကျေးဇူးတင်ပါတယ်ခင်ဗျာ။", reply_markup=main_menu_keyboard())
        except Exception as e:
            logging.error(f"Slip Error: {e}")
            bot.reply_to(message, "⚠️ Error ဖြစ်ပေါ်နေပါသည်။ Admin ID မှန်ကန်မှုရှိမရှိ စစ်ဆေးပါ။", reply_markup=main_menu_keyboard())
    else:
        msg = bot.send_message(message.chat.id, "⚠️ ကျေးဇူးပြု၍ ဓာတ်ပုံ (Screenshot) ကိုသာ ပေးပို့ပါ။ ပြန်လည်ပေးပို့ပေးပါခင်ဗျာ။", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(msg, process_slip_upload)

# ---------------------------------------------------------
# Menu Categories Callbacks (ပုံဖြုတ်ပြီး စာသားသီးသန့် ချက်ချင်းပေါ်အောင် ပြင်ဆင်ထားသည်)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def callback_menu_categories(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    order_markup = InlineKeyboardMarkup()
    order_markup.add(InlineKeyboardButton("🛒 ယခုမှာယူမည် (Order Now)", callback_data="action_order"))

    if call.data == "cat_drinks":
        desc = "🥤 **အအေး မျိုးစုံ**\n\n- ကော်ဖီ / တီး\n- သစ်သီးဖျော်ရည်များ\n- ဆိုဒါဖျော်ရည်များ\n\nအရသာရှိသော အအေးများကို မှာယူနိုင်ပါသည်။"
    elif call.data == "cat_chicken":
        desc = "🍗 **ကြက်ကင်**\n\n- ပျားရည်ဆမ်း ကြက်ကင်\n- ပုံမှန် ကြက်ကင်\n\nပူပူနွေးနွေး အရည်ရွှမ်းသော ကြက်ကင်လေး ရပါမယ်။"
    elif call.data == "cat_salad":
        desc = "🥗 **အသုတ်စုံများ**\n\n- ခေါက်ဆွဲသုတ်\n- ပဲပြားသုတ်\n- တို့ဘူးသုပ်အမျိုးမျိုး\n\nအရသာရှယ် အချဥ်စပ်လေး ရပါမယ်။"
    elif call.data == "cat_rice":
        desc = "🍚 **ထမင်းနှင့် ဟင်းလျာ**\n\n- ကြက်ဆီထမင်း\n- ဝက်သားနီချက်\n- ထမင်းကြော်အမျိုးမျိုး\n\nမွှေးကြိုင်လတ်ဆတ်သော ထမင်းဟင်းလျာများ ရပါပြီ။"
    elif call.data == "cat_noodle":
        desc = "🍜 **ခေါက်ဆွဲ/ကြာဆံ**\n\n- ရှမ်းခေါက်ဆွဲ\n- မြေအိုးမြီးရှည်\n- ကြာဆံကြော်\n\nပူပူနွေးနွေး အရည်သောက်နဲ့ အသုပ်တွေ ရပါမယ်။"
    elif call.data == "cat_dessert":
        desc = "🍰 **အချိုပွဲ**\n\n- ရေခဲမုန့်\n- သစ်သီးစုံပွဲ\n- ကိတ်မုန့်\n\nစားကောင်းပြီး ချိုမြိန်တဲ့ အချိုပွဲများ ဖြစ်ပါတယ်။"
    else:
        return

    # ပုံမပို့တော့ဘဲ Message အဖြစ်သာ ချက်ချင်းပို့ပေးမည်
    bot.send_message(chat_id, desc, reply_markup=order_markup, parse_mode='Markdown')

# ---------------------------------------------------------
# Table Booking Callback (Bug ပြင်ဆင်ပြီး)
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('book_table_'))
def callback_book_table(call):
    bot.answer_callback_query(call.id)
    table_no = call.data.split('_')[2]
    msg = bot.send_message(
        call.message.chat.id, 
        f"✅ **(စားပွဲ နံပါတ် - {table_no})** ကို ရွေးချယ်လိုက်ပါသည်။\n\n"
        "လူကြီးမင်း၏ **အမည်၊ ဖုန်းနံပါတ်၊ လာရောက်မည့် အချိန် နှင့် လူအရေအတွက်** ကို အောက်တွင် ရိုက်ပို့ပေးပါခင်ဗျာ။\n\n"
        "*(ဥပမာ - ဦးကျော်၊ 0912345678၊ ညနေ ၅ နာရီ၊ ၄ ယောက်)*", 
        reply_markup=cancel_keyboard(),
        parse_mode='Markdown'
    )
    # မှန်ကန်သော Parameter pass လုပ်နည်းဖြင့် ပြင်ဆင်ထားသည်
    bot.register_next_step_handler(msg, process_booking, table_no)

def process_booking(message, table_no):
    if message.text == '❌ ပယ်ဖျက်မည်':
        bot.send_message(message.chat.id, "Booking တင်ခြင်းကို ပယ်ဖျက်လိုက်ပါပြီ။", reply_markup=main_menu_keyboard())
        return

    admin_msg = (
        f"📅 **Booking အသစ် ဝင်လာပါပြီ** 📅\n\n"
        f"👤 Customer: {message.from_user.first_name}\n"
        f"📍 ရွေးချယ်ထားသောစားပွဲ: **စားပွဲ {table_no}**\n"
        f"📝 အသေးစိတ်:\n{message.text}"
    )
    try:
        bot.send_message(6146598194, admin_msg, parse_mode='Markdown')
        bot.reply_to(message, f"✅ (စားပွဲ {table_no}) အတွက် Booking တင်ခြင်း အောင်မြင်ပါသည်။ ဆိုင်မှ ပြန်လည်အတည်ပြု ဆက်သွယ်ပေးပါမည်။", reply_markup=main_menu_keyboard())
    except Exception as e:
        logging.error(f"Booking Error: {e}")
        bot.reply_to(message, "⚠️ Error ဖြစ်ပေါ်နေပါသည်၊ ဖုန်းဖြင့်သာ တိုက်ရိုက် ဆက်သွယ်ပေးပါ။", reply_markup=main_menu_keyboard())

# ---------------------------------------------------------
# Order Processing
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "action_order")
def callback_order(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    msg = bot.send_message(
        chat_id, 
        "📝 **အော်ဒါတင်ရန်**\n\nမှာယူလိုသော အစားအသောက်၊ အမည်၊ ဖုန်းနံပါတ် နှင့် ပို့ဆောင်ရမည့်လိပ်စာကို ရိုက်ထည့်ပေးပါခင်ဗျာ။", 
        reply_markup=cancel_keyboard(),
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_order)

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
        bot.reply_to(message, "✅ လူကြီးမင်း၏ အော်ဒါကို လက်ခံရရှိပါပြီ။ မကြာမီ ဆိုင်မှ စစ်ဆေးအတည်ပြုပေးပါမည်။ (ငွေပေးချေရန် ခလုတ်မှတစ်ဆင့်လည်း ရှင်းလင်းနိုင်ပါသည်)", reply_markup=main_menu_keyboard())
    except Exception as e:
        logging.error(f"Order Admin Alert Failed: {e}")
        bot.reply_to(message, "⚠️ အချက်အလက် ပို့ဆောင်ရာတွင် အဆင်မပြေဖြစ်သွားပါသည်။ ဖုန်းဖြင့် တိုက်ရိုက်ဆက်သွယ်ပေးပါ။", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith('status_'))
def handle_order_status(call):
    bot.answer_callback_query(call.id)
    data = call.data.split('_')
    action = data[1]
    customer_id = data[2]

    if action == "accept":
        bot.send_message(customer_id, "🎉 **သတင်းကောင်းပါ!**\nလူကြီးမင်း၏ အော်ဒါကို ဆိုင်မှ လက်ခံလိုက်ပါပြီ။ မကြာမီ ပြင်ဆင်ပို့ဆောင်ပေးပါမည်။")
        bot.edit_message_text(f"{call.message.text}\n\n🟢 **[Status: အော်ဒါလက်ခံပြီး]**", call.message.chat.id, call.message.message_id)
    elif action == "reject":
        bot.send_message(customer_id, "⚠️ **တောင်းပန်အပ်ပါသည်**\nလူကြီးမင်း၏ အော်ဒါမှာ ပစ္စည်းကုန်သွားခြင်း (သို့) ဆိုင်ပိတ်သွားခြင်းကြောင့် လက်မခံနိုင်တော့ပါခင်ဗျာ။")
        bot.edit_message_text(f"{call.message.text}\n\n🔴 **[Status: ပယ်ဖျက်လိုက်သည်]**", call.message.chat.id, call.message.message_id)

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
