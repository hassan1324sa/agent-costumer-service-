from crewai import LLM
from helpers.config import getSettings


class MakeLLm():
    def __init__(self,modelName:str,modelTemp:int=0):
        self.llmName=modelName
        self.llmTemp = modelTemp
    
    def getLLm(self):
        llm = LLM(
            model=self.llmName,            
            api_key=getSettings().COHERE_API_KEY,
            temperature=self.llmTemp
        )
        return llm



