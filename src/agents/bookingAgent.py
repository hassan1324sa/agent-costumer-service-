import json
import re
import aiohttp
import agentops
from helpers.config import getSettings
from stores.llms import MakeLLm
from controllers.bookingController import BookingController

settings = getSettings()
LLmOBJ = MakeLLm(settings.LLM_ROUTER, settings.LLM_TEMP)
llm = LLmOBJ.getLLm()

agentops.init(
    api_key=settings.AGENTOPS_API_KEY,
    skip_auto_end_session=True
)

controller = BookingController()


class BookingAgentManager:
    """
    Agent لإدارة عملية الحجز خطوة بخطوة،
    ويتعامل مع الـ API الخاص بـ FastAPI Booking.
    """

    def __init__(self, app):
        self.app = app
        self.sessions = {}
        self.api_url = f"{settings.FASTAPI_URL}/api/booking/add/"

    async def handle_booking(self, update, text: str) -> str:
        user_id = update.effective_user.id
        msg = text.strip()
        session = self.sessions.get(user_id)

        if not session:
            self.sessions[user_id] = {
                "stage": "ask_name",
                "data": {"username": None, "service_type": None, "date": None, "time": None},
            }
            return "أهلاً 👋 ممكن أعرف اسمك علشان نبدأ الحجز؟"

        stage = session["stage"]
        data = session["data"]

        if stage == "ask_name":
            data["username"] = msg
            session["stage"] = "ask_service"
            return f"تمام يا {data['username']} 😄، إيه نوع الكورس اللي حابب تحجزه؟"


        elif stage == "ask_service":
            data["service_type"] = msg
            session["stage"] = "ask_date"
            return "📅 إمتى تحب يكون الحجز؟ (YYYY-MM-DD)"
        
        elif stage == "ask_date":
            try:
                controller.validate_date(msg)  # التحقق من التاريخ
                data["date"] = msg
                session["stage"] = "ask_time"
                return "🕒 الساعة كام تحب الحجز يكون؟ (مثال: 15:30 أو 3:30 PM)"
            except Exception:
                return "⚠️ التاريخ مش مظبوط، اكتب بصيغة صحيحة"

        elif stage == "ask_time":
            try:
                controller.validate_time(msg)  # التحقق من الوقت
                data["time"] = msg
                session["stage"] = "confirm"
            except Exception:
                return "⚠️ الوقت مش مظبوط، اكتب مثال: 15:30 أو 3:30 PM"

            try:
                async with aiohttp.ClientSession() as http_session:
                    async with http_session.post(
                        self.api_url,
                        params={
                            "username": data["username"],
                            "service_type": data["service_type"],
                            "date": data["date"],
                            "time": data["time"]
                        },
                    ) as response:

                        res_data = await response.json()
                        if response.status == 200:
                            confirmation = (
                                f"✅ تم تأكيد حجزك بنجاح!\n\n"
                                f"👤 الاسم: {data['username']}\n"
                                f"📘 نوع الخدمة: {data['service_type']}\n"
                                f"📅 التاريخ: {data['date']}\n"
                                f"🕒 الوقت: {data['time']}\n\n"
                                f"شكرًا لاختيارك خدمتنا ❤️"
                            )
                        elif response.status == 409:
                            confirmation = "⚠️ الحجز موجود بالفعل لنفس الوقت والخدمة."
                        else:
                            error_msg = res_data.get("detail") or res_data.get("signal", "حدث خطأ غير متوقع.")
                            confirmation = f"❌ حصل خطأ أثناء تسجيل الحجز: {error_msg}"

            except Exception as e:
                confirmation = f"❌ حصل خطأ أثناء تجهيز الحجز: {e}"

            self.sessions.pop(user_id, None)
            return confirmation

        # fallback
        self.sessions[user_id] = {
            "stage": "ask_name",
            "data": {"username": None, "service_type": None, "date": None, "time": None},
        }
        return "خلينا نبدأ من الأول 😊 ممكن تقولّي اسمك؟"
