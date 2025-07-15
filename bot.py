import csv
import os
import sqlite3
import gspread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from google.oauth2.service_account import Credentials
import json

# Отримаємо JSON з env
creds_json = os.getenv("GOOGLE_CREDS_JSON")

# Створимо тимчасовий файл
with open("creds.json", "w") as f:
    f.write(creds_json)

# Вкажи обсяг доступу
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Путь до JSON-файлу з ключем
creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)

# Авторизація через gspread
gc = gspread.authorize(creds)

# Відкриття таблиці за назвою
sheet = gc.open_by_key("1EQq7u8BaqboIdgS7E5c0vj0fLQLO-UtbPpdESF9ojyY").sheet1

NAME, CONTACT, COMMENT = range(3)

# Стадії для тесту
Q1, Q2, Q3 = range(3)
T1_Q1, T1_Q2, T1_Q3, T1_Q4, T1_Q5 = range (5)

TOKEN = os.getenv("TOKEN")


# Зберігаємо тимчасово відповіді користувача у словнику (у context.user_data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙌 Привіт! Я бот мислиця!\n\n" \
        "Змінімо цей світ на краще, розвиваючи критичне мислення.\n\n" \
        "💙 Напиши /critical, щоб пройти тест на критичне мислення.\n\n" \
        "💙 Напиши /apply, щоб подати заявку."
    )

# --- Обробка заявки ---
async def apply_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введи своє ім'я:")
    return NAME

async def apply_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введи свій контакт (телефон або email):")
    return CONTACT

async def apply_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contact'] = update.message.text
    await update.message.reply_text("Напиши короткий коментар або повідомлення:")
    return COMMENT

async def apply_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['comment'] = update.message.text

    # Записуємо у CSV файл
    # with open("zayavky.csv", "a", newline="", encoding="utf-8") as f:
    #     writer = csv.writer(f)
    #     writer.writerow([
    #         update.effective_user.id,
    #         context.user_data['name'],
    #         context.user_data['contact'],
    #         context.user_data['comment']
    #     ])
    # Записуємо у Google таблицю
    sheet.append_row([
        str(update.effective_user.id),
        context.user_data['name'],
        context.user_data['contact'],
        context.user_data['comment']
    ])

    await update.message.reply_text("Дякуємо! Заявку прийнято ✅")
    return ConversationHandler.END

async def apply_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заявка скасована.")
    return ConversationHandler.END

# --- Обробка тесту ---
async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Ні", callback_data="q1_Ni"), InlineKeyboardButton("Так", callback_data="q1_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Питання 1: Чи можна вважати всі повідомлення у ЗМІ об'єктивними та достовірними?",
        reply_markup=reply_markup
    )
    return Q1

async def test_q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q1'] = query.data.split('_')[1]  # Отримаємо "Tak" чи "Ni"

    keyboard = [
        [InlineKeyboardButton("Ні", callback_data="q2_Ni"), InlineKeyboardButton("Так", callback_data="q2_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "Питання 2: Чи потрібно перевіряти інформацію з кількох джерел, щоб скласти повну картину?",
        reply_markup=reply_markup
    )
    return Q2

async def test_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q2'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Ні", callback_data="q3_Ni"), InlineKeyboardButton("Так", callback_data="q3_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "Питання 3: Чи потрібно враховувати протилежні точки зору при аналізі інформації?",
        reply_markup=reply_markup
    )
    return Q3

async def test_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q3'] = query.data.split('_')[1]

    # Перевірка відповідей (приклад)
    correct_answers = {'q1': 'Ni', 'q2': 'Tak', 'q3': 'Tak'}
    results = []
    for q in ['q1', 'q2', 'q3']:
        user_answer = context.user_data.get(q)
        correct = "✅" if user_answer == correct_answers[q] else "❌"
        results.append(f"{q.upper()}: {user_answer} {correct}")

    await query.message.reply_text(
        "Дякую за відповіді!\n" + "\n".join(results)
    )
    return ConversationHandler.END

async def test_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тест скасовано.")
    return ConversationHandler.END

# --- Обробка тесту 1 ---
async def critical_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Фейк", callback_data="q1_Ni"), InlineKeyboardButton("Правда", callback_data="q1_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔵 Визнач: «Наступний факт є фейком чи правдою?»",
    )
    await update.message.reply_text(
        "1. Критичне мислення допомагає розрізняти факти і припущення.",
        reply_markup=reply_markup
    )
    return T1_Q1

async def critical_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q1'] = query.data.split('_')[1]  # Отримаємо "Tak" чи "Ni"

    keyboard = [
        [InlineKeyboardButton("Фейк", callback_data="q2_Ni"), InlineKeyboardButton("Правда", callback_data="q2_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "2. Критичне мислення — це постійна недовіра до всіх і всього.",
        reply_markup=reply_markup
    )
    return T1_Q2

async def critical_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q2'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Фейк", callback_data="q3_Ni"), InlineKeyboardButton("Правда", callback_data="q3_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "3. Людина з критичним мисленням ніколи не погоджується з думкою інших.",
        reply_markup=reply_markup
    )
    return T1_Q3

async def critical_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q3'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Фейк", callback_data="q4_Ni"), InlineKeyboardButton("Правда", callback_data="q4_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "4. Критичне мислення — це навичка, яку можна тренувати і вдосконалювати.",
        reply_markup=reply_markup
    )
    return T1_Q4

async def critical_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q4'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Фейк", callback_data="q5_Ni"), InlineKeyboardButton("Правда", callback_data="q5_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "5. Критичне мислення полягає лише в тому, щоб знати більше фактів..",
        reply_markup=reply_markup
    )
    return T1_Q5

async def critical_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()
    context.user_data['q5']=query.data.split('_')[1]

    correct_answers={
        'q1':'Tak',
        'q2':'Ni',
        'q3':'Ni',
        'q4':'Tak',
        'q5':'Ni'
    }

    correct_answer_print={
        'Tak':'Правда',
        'Ni':'Фейк'
    }
    l=len(context.user_data)
    result=[]
    score=0
    for q in [f'q{i}'for i in range(1,l+1) ]:
        u_ans=context.user_data[q]
        c_ans=correct_answers[q]
        if u_ans==c_ans:
            correct="✅"
            score+=1
        else:
            correct="❌"
        result.append(q.upper()+":"+correct+"\n"+
                      f'🔹 Твоя відповідь: {correct_answer_print[u_ans]}\n'+
                      f'▫️ Правильна відповідь: {correct_answer_print[c_ans]}\n')
    await query.message.reply_text(
        "Дякую за відповіді!\n"+f'Ось твої результати: {score}/{l}\n\n'+'\n'.join(result)
    )
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Конверсаційний хендлер для заявки
    apply_conv = ConversationHandler(
        entry_points=[CommandHandler('apply', apply_start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, apply_name)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, apply_contact)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, apply_comment)],
        },
        fallbacks=[CommandHandler('cancel', apply_cancel)]
    )

    # Конверсаційний хендлер для тесту
    test_conv = ConversationHandler(
        entry_points=[CommandHandler('test', test_start)],
        states={
            Q1: [CallbackQueryHandler(test_q1, pattern='^q1_')],
            Q2: [CallbackQueryHandler(test_q2, pattern='^q2_')],
            Q3: [CallbackQueryHandler(test_q3, pattern='^q3_')],
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )
        # Конверсаційний хендлер для тесту
    critical_conv = ConversationHandler(
        entry_points=[CommandHandler('critical', critical_start)],
        states={
            T1_Q1: [CallbackQueryHandler(critical_q2, pattern='^q1_')],
            T1_Q2: [CallbackQueryHandler(critical_q3, pattern='^q2_')],
            T1_Q3: [CallbackQueryHandler(critical_q4, pattern='^q3_')],
            T1_Q4: [CallbackQueryHandler(critical_q5, pattern='^q4_')],
            T1_Q5: [CallbackQueryHandler(critical_end, pattern='^q5_')],
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(apply_conv)
    app.add_handler(test_conv)
    app.add_handler(critical_conv)

    print("Бот запущено")
    app.run_polling()
