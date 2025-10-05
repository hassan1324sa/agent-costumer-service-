from bson import ObjectId
from datetime import datetime

def bson_to_json(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()  # يحوله إلى string بشكل قياسي
    if isinstance(obj, list):
        return [bson_to_json(item) for item in obj]
    if isinstance(obj, dict):
        return {key: bson_to_json(value) for key, value in obj.items()}
    return obj
