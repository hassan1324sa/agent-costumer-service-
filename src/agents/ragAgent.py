from crewai import Agent, Task
from crewai.tools import tool
import agentops
from stores.llms import MakeLLm

class RAGAgentManager:
    def __init__(self, app):
        self.settings = app.settings
        self.qdrant = app.qdrant
        self.cohere_client = app.cohere_client

        LLmOBJ = MakeLLm(self.settings.LLM_ROUTER, self.settings.LLM_TEMP)
        self.llm = LLmOBJ.getLLm()

        agentops.init(api_key=self.settings.AGENTOPS_API_KEY, skip_auto_end_session=True)

        self.kb_tool = self.create_kb_tool()
        self.rag_agent = self.create_rag_agent()
        self.rag_task = self.create_rag_task()

    def create_kb_tool(self):
        @tool
        def kb_tool(query: str) -> str:
            """
            تبحث في قاعدة المعرفة باستخدام الـ embeddings من Cohere.
            ترجع أفضل 5 نتائج مرتبطة بالاستعلام.
            لو مفيش نتائج، ترجع رسالة: 'للأسف، معرفش أي معلومة عن سؤالك.'
            """
            try:
                if not self.qdrant.isCollectionExisted("rag_data"):

                    return "للأسف، معرفش أي معلومة عن سؤالك."

                response = self.cohere_client.embed(
                    model="embed-multilingual-v3.0",
                    texts=[query],
                    input_type="search_query"
                )
                query_vector = response.embeddings[0]

                results = self.qdrant.searchByVector(
                    collectionName="rag_data",
                    vector=query_vector,
                    limit=5
                )

                if not results:
                    return "للأسف، معرفش أي معلومة عن سؤالك."

                retrieved_texts = [f"{i+1}. {doc.text}" for i, doc in enumerate(results)]
                return "\n".join(retrieved_texts)

            except Exception as e:
                print(f"❌ Error in knowledge_base_search: {e}")
                return "للأسف، معرفش أي معلومة عن سؤالك."

        return kb_tool

    def create_rag_agent(self):
        return Agent(
            role="وكيل استرجاع المعرفة (RAG)",
            goal="تقديم إجابات دقيقة فقط بناءً على قاعدة المعرفة.",
            backstory=(
                "خبير في استرجاع المعلومات من قاعدة البيانات الشعاعية باستخدام embeddings من Cohere. "
                "لو مفيش بيانات في قاعدة المعرفة، لا تجيب من عندك وقول فقط: 'للأسف، معرفش أي معلومة عن سؤالك.'"
            ),
            llm=self.llm,
            tools=[self.kb_tool]
        )

    def create_rag_task(self):
        return Task(
            description="""
                خليك لطيف.
                استخدم الأداة kb_tool لاسترجاع المعلومات من قاعدة المعرفة.
                لو رجعت None أو كانت النتيجة فارغة، قول فقط: 'للأسف، معرفش أي معلومة عن سؤالك.'
                لو لقيت بيانات، استخدمها لإنشاء إجابة دقيقة وواضحة.
                ممنوع تجاوب من نفسك بدون بيانات من قاعدة المعرفة، وممنوع ذكر اسم الأداة.
            """,
            expected_output="إجابة نصية دقيقة أو 'للأسف، معرفش أي معلومة عن سؤالك.'",
            agent=self.rag_agent
        )
