from crewai import Agent, Task
import agentops
from helpers.config import getSettings
from stores.llms import MakeLLm

settings = getSettings()


LLmOBJ= MakeLLm(settings.LLM_ROUTER,settings.LLM_TEMP) 
llm = LLmOBJ.getLLm()

agentops.init(
    api_key=getSettings().AGENTOPS_API_KEY,
    skip_auto_end_session=True
)
router_agent = Agent(
    role="وكيل التوجيه",
    goal="تحليل نية المستخدم وتحديد إذا كانت الرسالة سؤال عام (FAQ) أو طلب حجز (Booking).",
    backstory="وكيل ذكي مسؤول عن تصنيف نية المستخدم بدقة.",
    llm=llm
)

router_task = Task(
    description="""
        حلل الرسالة النصية القادمة من المستخدم لتحديد النية.
        لو الرسالة تتكلم عن سؤال عام (مثل الأسعار، المواعيد، الخدمات...) خلي 'faq' = true و 'booking' = false.
        لو الرسالة فيها نية حجز (مثل أحجز، حجز، موعد...) خلي 'faq' = false و 'booking' = true.
        لو مش واضح نوع الرسالة، خلي الاثنين false.
        الناتج لازم يكون في صيغة JSON فقط بدون أي شرح إضافي.
    """,
    expected_output='{"faq": true|false, "booking": true|false}',
    agent=router_agent
)