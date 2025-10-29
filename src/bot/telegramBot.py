import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from agents.routerAgent import router_agent, router_task
from agents.bookingAgent import BookingAgentManager
from agents.ragAgent import RAGAgentManager
import asyncio
import json
import re

rag_manager_instance = None
booking_manager_instance = None

request = HTTPXRequest(connect_timeout=20, read_timeout=20)

async def receive_msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE, app=None):
    global rag_manager_instance, booking_manager_instance
    text = update.message.text.strip()
    user_id = update.effective_user.id

    try:
        if booking_manager_instance and user_id in booking_manager_instance.sessions:
            result = await booking_manager_instance.handle_booking(update, text)
            await update.message.reply_text(result)
            return

        router_output = router_task.execute_sync(context=text, agent=router_agent)
        raw_output = router_output.dict().get("raw", "").strip()
        cleaned_output = re.sub(r"```(?:json)?", "", raw_output).strip().strip("`").strip()

        if cleaned_output.startswith("{") and cleaned_output.endswith("}"):
            router_dict = json.loads(cleaned_output)

            if router_dict.get("greeting"):
                await update.message.reply_text(
                    "أهلاً وسهلاً! 😊 منورنا يا جميل 🌟\n"
                    "تقدر تسألني عن خدماتنا أو تعمل حجز لو حابب 💬"
                )
                return

            elif router_dict.get("faq"):
                if rag_manager_instance is None:
                    rag_manager_instance = RAGAgentManager(app=app)

                result = rag_manager_instance.ask(text)
                await update.message.reply_text(str(result))
                return

            elif router_dict.get("booking"):
                if booking_manager_instance is None:
                    booking_manager_instance = BookingAgentManager(app=app)

                result = await booking_manager_instance.handle_booking(update, text)
                await update.message.reply_text(result)
                return

            else:
                await update.message.reply_text("مش قادر أحدد الرسالة 😅، ممكن توضّحلي أكتر؟")
                return

        else:
            await update.message.reply_text(cleaned_output)

    except Exception as e:
        print(f"❌ خطأ أثناء معالجة الرسالة: {e}")
        await update.message.reply_text("في مشكلة بسيطة حصلت 😔، جرّب تبعتلي تاني.")


async def runBot(app):
    """تشغيل البوت."""
    BOT_TOKEN = app.settings.BOT_TOKEN
    tg_app = Application.builder().token(BOT_TOKEN).request(request).build()

    tg_app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, ctx: receive_msg(update, ctx, app))
    )

    await tg_app.initialize()
    await tg_app.start()
    print("🤖 Telegram bot started successfully!")

    asyncio.create_task(tg_app.updater.start_polling())
    return tg_app
