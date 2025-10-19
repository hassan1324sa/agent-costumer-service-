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

        self.summary_memory = "لا يوجد تلخيص بعد."

        agentops.init(
            api_key=self.settings.AGENTOPS_API_KEY,
            skip_auto_end_session=True
        )

    def kb_tool(self, query: str) -> str:
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

            retrieved_texts = [doc.text for doc in results]
            return "\n\n".join(retrieved_texts)

        except Exception as e:
            print(f"❌ Error in knowledge_base_search: {e}")
            return "للأسف، معرفش أي معلومة عن سؤالك."

    def build_prompt(self, query: str, context_docs: str) -> str:
        prompt = f"""
        أنت مساعد ذكي. جاوب بدقة اعتمادًا على المعلومات والسياق والتلخيص السابق للمحادثة.
        لو مفيش معلومة كافية جاوب: "للأسف، معرفش أي معلومة عن سؤالك."

        🧠 التلخيص السابق:
        {self.summary_memory}

        🧩 السياق من قاعدة المعرفة:
        {context_docs}

        ❓ السؤال الحالي:
        {query}

        ✍️ الإجابة:
        """
        return prompt.strip()

    def update_summary(self, query: str, answer: str):
        try:
            summarization_prompt = f"""
            التلخيص الحالي للمحادثة:
            {self.summary_memory}

            آخر تفاعل:
            - المستخدم: {query}
            - المساعد: {answer}

            رجّع تلخيص جديد مختصر ودقيق يضم أهم النقاط فقط.
            """
            response = self.llm.call(summarization_prompt)

            if isinstance(response, dict) and "text" in response:
                self.summary_memory = response["text"].strip()
            else:
                self.summary_memory = str(response).strip()
        except Exception as e:
            print(f"❌ Error updating summary: {e}")

    def ask(self, query: str) -> str:
        try:
            context_docs = self.kb_tool(query)
            if "للأسف، معرفش" in context_docs:
                return context_docs

            prompt = self.build_prompt(query, context_docs)
            response = self.llm.call(prompt)

            if isinstance(response, dict) and "text" in response:
                answer = response["text"]
            else:
                answer = str(response).strip()

            self.update_summary(query, answer)

            return answer

        except Exception as e:
            print(f"❌ Error in RAG ask(): {e}")
            return "حصل خطأ أثناء المعالجة."
