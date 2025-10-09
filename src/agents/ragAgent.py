from crewai import Agent
from agents.bookingAgent import handle_booking
from agents.ragAgent import handle_rag

router_agent = Agent(
    name="Router Agent",
    role="Classifier",
    goal="تحديد نوع الطلب وإرساله للـ Agent المناسب.",
    backstory="خبير في تحليل نية المستخدم.",
    llm="cohere",
)

def classify_message(msg: str):
    msg_lower = msg.lower()
    if "احجز" in msg_lower or "booking" in msg_lower:
        return "booking"
    return "rag"

async def handle_router(message: str):
    task_type = classify_message(message)
    if task_type == "booking":
        return await handle_booking(message)
    else:
        return await handle_rag(message)
