# Description: This file contains utility functions that are used in the application.
from bson import ObjectId
import json

# Used to encode MongoDB ObjectIds to strings for JSON serialization
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

# Convert an object to JSON-serializable format by handling MongoDB ObjectIds
def prepare_for_json(obj):
    if isinstance(obj, list):
        return [prepare_for_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: prepare_for_json(v) for k, v in obj.items()}
    elif hasattr(obj, '_id'):
        # Convert ObjectId to string if it exists
        if hasattr(obj._id, '__str__'):
            obj._id = str(obj._id)
        return obj
    else:
        return obj