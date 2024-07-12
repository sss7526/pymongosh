import json
from bson import ObjectId, Decimal128, Binary
from datetime import datetime
from uuid import UUID
import base64

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Binary):
            return base64.b64encode(obj).decode('utf-8')
        if isinstance(obj, Decimal128):
            return str(obj)
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
