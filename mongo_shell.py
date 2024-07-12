from pymongo import MongoClient, InsertOne
from pymongo.errors import PyMongoError
from bson import ObjectId, Decimal128, Binary
from datetime import datetime
from uuid import UUID
import json

class MongoShell:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = None

    def list_databases(self):
        
        try:
            return self.client.list_database_names()
        
        except PyMongoError as e:
            return f'Error listing databases: {str(e)}'
        
    def use_database(self, db_name):
        
        try:
            self.db = self.client[db_name]
            return f'Using database: {db_name}'
        
        except PyMongoError as e:
            return f'Error switching database: {str(e)}'
        
    def list_collections(self):
        if self.db is None:
            return "No database selected. Use '<database_name>' to select a database."
        
        try:
            return self.db.list_collection_names()
        
        except PyMongoError as e:
            return f'Error listing collection: {str(e)}'
        
    def execute_query(self, collection, query):
        if self.db is None:
            return "No database selected. Use 'use <database_name>' to select a database."

        try:
            collection = self.db[collection]
            result = collection.find(query)
            return list(result)
        
        except PyMongoError as e:
            return f'Error executing query: {str(e)}'
        
        except Exception as e:
            return f'Invalid query format: {str(e)}'
        
    def execute_command(self, command):
        if self.db is None:
            return "No database selected. Use 'use <database_name>' to select a database."
        
        try:
            result = self.db.command(command)
            return result
        
        except PyMongoError as e:
            return f'Error executing command: {str(e)}'
        
        except Exception as e:
            return f'Invalid command format: {str(e)}'
        
    def insert_document(self, collection, document):
        if self.db is None:
            return "No database selected. Use 'use <database_name>' to select a database."
        
        try:
            document_dict = json.loads(document, object_hook=self.bson_object_hook)
            collection = self.db[collection]
            result = collection.insert_one(document_dict)
            return {'_id', str(result.inserted_id)}
        
        except PyMongoError as e:
            return f'Error inserting document: {str(e)}'
        
        except json.JSONDecodeError as e:
            return f'Invalid JSON format: {str(e)}'
        
        except Exception as e:
            return f'Error: {str(e)}'
    
    def bson_object_hook(self, dct):
        for key, value in dct.items():
            if isinstance(value, dict):
                if "$oid" in value:
                    dct[key] = ObjectId(value["$oid"])
                elif "$date" in value:
                    dct[key] = datetime.fromisoformat(value["$date"].replace("Z", "+00:00"))
                elif "$binary" in value:
                    dct[key] = Binary(bytes.fromhex(value["$binary"]))
                elif "$numberDecimal" in value:
                    dct[key] = Decimal128(value["$numberDecimal"])
                elif "$uuid" in value:
                    dct[key] = Binary.from_uuid(UUID(value["$uuid"]))
        return dct

    def close(self):
        self.client.close()
