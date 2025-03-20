import telegram
from telegram.ext import Application, CommandHandler, ContextTypes
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Токен від BotFather
TOKEN = "7556880415:AAEK3n9nGp0zTpc0CAzJHf1KJ3CWpr7hZf8"  # Заміни на свій токен

# Підключення до Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("timebot-454309-cb430b2a3699.json", scope)  # Заміни на свій JSON-файл
client = gspread.authorize(creds)
sheet = client.open("Tasks").sheet1

async def start(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот для тайм-менеджменту. Напиши /add, щоб додати завдання, або /list, щоб побачити список.")

async def add_task(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    task = " ".join(context.args)
    if not task:
        await update.message.reply_text("Напиши задачу після /add, наприклад: /add Зробити звіт 14:00")
        return
    try:
        time = task.split()[-1]
        task_text = " ".join(task.split()[:-1])
        sheet.append_row([user_id, task_text, time])
        await update.message.reply_text(f"Додано: {task_text} на {time}")
    except:
        await update.message.reply_text("Щось пішло не так. Формат: /add Задача Час")

async def list_tasks(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    records = sheet.get_all_values()
    user_tasks = [row for row in records if row[0] == user_id]
    if not user_tasks:
        await update.message.reply_text("У тебе немає завдань.")
    else:
        response = "Твої завдання:\n"
        for row in user_tasks:
            response += f"- {row[1]} ({row[2]})\n"
        await update.message.reply_text(response)

async def tip(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Порада: Починай день із найскладнішого завдання, щоб зняти стрес.")

def main():
    # Створюємо Application замість Updater
    application = Application.builder().token(TOKEN).build()

    # Додаємо обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("list", list_tasks))
    application.add_handler(CommandHandler("tip", tip))

    # Запускаємо бота
    application.run_polling(allowed_updates=telegram.Update.ALL_TYPES)

if __name__ == "__main__":
    main()