from fastapi import UploadFile
from models.enums.responseEnum import ResponseEnum
import re 
import os 


class DataController():
    def __init__(self):
        pass


    def validateData(self,question:str):
        if isinstance(question,str):
            return True,ResponseEnum.validationPassed
        return False,ResponseEnum.validationError
