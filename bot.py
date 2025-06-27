import csv
import os
import gspread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from google.oauth2.service_account import Credentials

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

TOKEN = os.getenv("TOKEN")


# Зберігаємо тимчасово відповіді користувача у словнику (у context.user_data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙌 Привіт! Я бот мислиця!\n\n" \
        "Змінімо цей світ на краще, розвиваючи критичне мислення. " \
        "\n\n🌸 Напиши /test, щоб пройти тест та спробувати себе у аналізі інформації.\n\n🌸 Напиши /apply, щоб подати заявку."
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

    app.add_handler(CommandHandler("start", start))
    app.add_handler(apply_conv)
    app.add_handler(test_conv)

    print("Бот запущено")
    app.run_polling()
