from helpers.config import getSettings
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from agents.routerAgent import router_agent, router_task

BOT_TOKEN = getSettings().BOT_TOKEN

async def receive_msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text
    chat = update.effective_chat

    print(f"[{chat.id}] {user.first_name}: {text}")

    try:
        router_output = router_task.execute_sync(context=text, agent=router_agent)
        print(f"نتيجة التوجيه: {router_output}")
        await update.message.reply_text(str(router_output))
    except Exception as e:
        print(f"خطأ في تنفيذ الوكلاء: {e}")
        await update.message.reply_text(f"حدث خطأ أثناء معالجة الرسالة: {str(e)}")

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_msg))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()