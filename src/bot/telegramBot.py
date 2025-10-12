from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from agents.routerAgent import router_agent, router_task
from agents.ragAgent import rag_agent, rag_task
from helpers.config import getSettings
import asyncio
import json 
import re

# from agents.ragAgent import rag_task

BOT_TOKEN = getSettings().BOT_TOKEN
async def receive_msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text
    chat = update.effective_chat
    
    try:
        router_output = router_task.execute_sync(context=text, agent=router_agent)
        routerDict= router_output.dict()["raw"]
        cleanedRouterDict = re.sub(r"```(?:json)?", "", routerDict).strip().strip("`").strip()
        routerDict = json.loads(cleanedRouterDict)
        if routerDict["faq"]:
            rag_output = rag_task.execute_sync(context=text, agent=rag_agent)
            print(text)
            print(rag_output)
            await update.message.reply_text(str(rag_output))
        
    except Exception as e:
        print(f"خطأ في تنفيذ الوكلاء: {e}")
        await update.message.reply_text(f"حدث خطأ أثناء معالجة الرسالة: {str(e)}")

async def runBot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_msg))

    loop = asyncio.get_event_loop()
    await app.initialize()
    await app.start()
    print("🤖 Telegram bot started successfully!")

    asyncio.create_task(app.updater.start_polling())
