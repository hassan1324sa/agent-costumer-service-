from helpers.config import getSettings
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = getSettings().BOT_TOKEN


async def receive_msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text
    chat = update.effective_chat

    print(f"[{chat.id}] {user.first_name}: {text}")

    await update.message.reply_text(f"احا: {text}")

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_msg))

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()





