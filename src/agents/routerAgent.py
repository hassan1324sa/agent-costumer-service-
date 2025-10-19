from crewai import Agent, Task
import agentops
from helpers.config import getSettings
from stores.llms import MakeLLm

settings = getSettings()

LLmOBJ = MakeLLm(settings.LLM_ROUTER, settings.LLM_TEMP)
llm = LLmOBJ.getLLm()

agentops.init(
    api_key=settings.AGENTOPS_API_KEY,
    skip_auto_end_session=True
)

router_agent = Agent(
    role="وكيل التوجيه",
    goal="فهم نية المستخدم بدقة والرد عليه بطريقة ودودة وبسيطة، سواء كانت تحية أو سؤال عام أو طلب حجز.",
    backstory="وكيل ذكي لطيف ومهذب، دايمًا بيرد على المستخدم بشكل مختصر ومباشر من غير أي تفكير بصوت عالي أو شرح.",
    llm=llm
)

router_task = Task(
    description="""
        مطلوب منك تحليل الرسالة النصية القادمة من المستخدم وتحديد نوعها بدقة.

        الحالات الممكنة:
        1. لو الرسالة فيها تحية (زي: مرحباً، السلام عليكم، هاي، أهلاً، صباح الخير...)
           → رد على المستخدم بلطافة، زي مثلاً:
             "أهلاً بيك! 😊 تقدر تسألني عن خدماتنا أو تعمل حجز لو حابب."

        2. لو الرسالة سؤال عام (زي الأسعار، المواعيد، الخدمات...)
           → الناتج لازم يكون JSON فقط بالشكل التالي:
             {"faq": true, "booking": false, "greeting": false}

        3. لو الرسالة فيها نية حجز (زي أحجز، حجز، موعد...)
           → الناتج لازم يكون JSON فقط بالشكل التالي:
             {"faq": false, "booking": true, "greeting": false}

        4. لو مش واضح نوع الرسالة
           → {"faq": false, "booking": false, "greeting": false}

        ⚠️ تعليمات مهمة:
        - الرد النهائي فقط بدون أي كلام إضافي أو تفكير.
        - لا تكتب "thinking" أو أي نص توضيحي.
        - لو الرد JSON، لازم يكون بالشكل المحدد بالضبط.
        - لو الرد نصي (تحية)، يكون بسيط ومهذب وودي.
    """,
    expected_output='إما رد نصي ودود أو {"faq": true|false, "booking": true|false, "greeting": true|false}',
    agent=router_agent
)
