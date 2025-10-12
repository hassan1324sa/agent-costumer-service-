# bot/telegramBot.py
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from agents.routerAgent import router_agent, router_task
from agents.ragAgent import RAGAgentManager
import asyncio
import json
import re

rag_manager_instance = None  # هنعمل instance واحد فقط

async def receive_msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE, app=None):
    global rag_manager_instance
    text = update.message.text
    try:
        # نحدد نوع الرسالة
        router_output = router_task.execute_sync(context=text, agent=router_agent)
        routerDict = router_output.dict()["raw"]
        cleanedRouterDict = re.sub(r"```(?:json)?", "", routerDict).strip().strip("`").strip()
        routerDict = json.loads(cleanedRouterDict)

        if routerDict.get("faq"):
            if rag_manager_instance is None:
                rag_manager_instance = RAGAgentManager(app=app)

            # هنا بنشغل الـ Task بتاع الـ Agent
            rag_output = rag_manager_instance.rag_task.execute_sync(
                context=text,
                agent=rag_manager_instance.rag_agent
            )
            result = rag_output  # الرد النهائي
        else:
            result = "الرد على هذا النوع من الرسائل غير مفعل حاليًا."

        await update.message.reply_text(str(result))

    except Exception as e:
        print(f"خطأ أثناء معالجة الرسالة: {e}")
        await update.message.reply_text(f"حدث خطأ أثناء معالجة الرسالة: {str(e)}")


async def runBot(app):
    BOT_TOKEN = app.settings.BOT_TOKEN
    tg_app = Application.builder().token(BOT_TOKEN).build()

    tg_app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        lambda update, ctx: receive_msg(update, ctx, app)
    ))

    await tg_app.initialize()
    await tg_app.start()
    print("🤖 Telegram bot started successfully!")

    asyncio.create_task(tg_app.updater.start_polling())