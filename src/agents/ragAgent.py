from crewai import Agent, Task
from crewai.tools import tool
import agentops
from helpers.config import getSettings
from stores.llms import MakeLLm
from stores.vectordb.providers.QdrantDB import QdrantDB
from stores.vectordb.vectorDBEnum import DistanceMethodEnums
import cohere

settings = getSettings()

LLmOBJ = MakeLLm(settings.LLM_ROUTER, settings.LLM_TEMP)
llm = LLmOBJ.getLLm()

agentops.init(
    api_key=settings.AGENTOPS_API_KEY,
    skip_auto_end_session=True
)

qdrant = QdrantDB(
    dbPath=settings.VDB_PATH,
    distanceMethod=DistanceMethodEnums.COSINE.value
)

cohereClient = cohere.Client(settings.COHERE_API_KEY)


@tool
def knowledge_base_search(query: str) -> str:
    """
    تبحث في قاعدة المعرفة باستخدام الـ embedding من Cohere،
    وترجع النتائج المرتبطة بالاستعلام.
    """
    try:
        qdrant.connect()

        response = cohereClient.embed(
            model="embed-multilingual-v3.0",
            texts=[query],
            input_type="search_query"
        )
        query_vector = response.embeddings[0]

        results = qdrant.searchByVector(
            collectionName="rag_data",
            vector=query_vector,
            limit=5
        )
        print(results)
        if not results or len(results) == 0:
            return "__NO_RESULTS__"

        retrieved_texts = []
        for i, doc in enumerate(results, start=1):
            retrieved_texts.append(f"{i}. (Score: {round(doc.score, 3)}) {doc.text}")

        output = "نتائج البحث:\n" + "\n".join(retrieved_texts)
        return output

    except Exception as e:
        print(f"❌ Error in knowledge_base_search: {e}")
        return "__ERROR__"

    finally:
        qdrant.disconnect()


rag_agent = Agent(
    role="وكيل استرجاع المعرفة (RAG)",
    goal="تقديم إجابات دقيقة فقط بناءً على قاعدة المعرفة.",
    backstory=(
        "خبير في استرجاع المعلومات من قاعدة البيانات الشعاعية باستخدام embeddings من Cohere. "
        "لو مفيش بيانات في قاعدة المعرفة، لا تجيب من عندك وقول فقط إنك لا تعرف."
    ),
    llm=llm,
    tools=[knowledge_base_search]
)

rag_task = Task(
    description="""
        استخدم الأداة knowledge_base_search لاسترجاع المعلومات من قاعدة المعرفة.
        لو رجعت "__NO_RESULTS__"، قول فقط: "معرفش إجابة السؤال ده لأن مفيش بيانات كفاية في قاعدة المعرفة."
        أما لو لقيت نتائج، استخدمها لإنشاء إجابة دقيقة وواضحة.
        ممنوع تجاوب من نفسك بدون بيانات من قاعدة المعرفة.
    """,
    expected_output="إجابة نصية دقيقة أو 'معرفش إجابة السؤال ده'.",
    agent=rag_agent
)