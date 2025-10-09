from helpers.config import getSettings,Settings
import os ,random,string

class BaseController:
    def __init__(self):
        self.appSettings=getSettings()
        self.baseDir = os.path.dirname( os.path.dirname(__file__) )
        self.filesDir= os.path.join(self.baseDir,"assets/files")
        self.databaseDir = os.path.join(
            self.baseDir,
            "assets/database"
        )

        
    def generateRandomString(self,length:int=12):
        return ''.join(random.choices(string.ascii_lowercase+string.digits,k=length))
    
    def getDatabasePath(self,dbName):
        databasePath=os.path.join(self.databaseDir,dbName)
        if not os.path.exists(databasePath):
            os.mkdir(path=databasePath)
            _ = os.makedirs(databasePath)
        return databasePath