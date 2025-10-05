from helpers.config import getSettings , Settings


class BaseDataModel:
    def __init__(self,dbClient:object):
        self.dbClient = dbClient
        self.appSettings = getSettings