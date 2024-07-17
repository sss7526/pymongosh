import pymongo

class DBProxy:
    def __init__(self, mongo_shell):
        self.mongo_shell = mongo_shell
        self.is_db_command = False

    def __getattr__(self, name):
        if self.mongo_shell.db is None:
            raise Exception("No database selecte. Use 'use <database_name>' to select a database")
        
        # Proxy the collection attribute
        collection = getattr(self.mongo_shell.db, name)
        if collection is not None:
            return MethodProxy(collection)
        raise AttributeError(f"'DBProxy' ojbect has no attribute '{name}'")
    
class MethodProxy:
    def __init__(self, collection):
        self.collection = collection

    def __getattr__(self, name):
        # Proxy the method call on the collection
        method = getattr(self.collection, name)

        def wrapper(*args, **kwargs):
            # Execute the method
            result = method(*args, **kwargs)

            # Check return type and format if necessary
            if isinstance(result, pymongo.cursor.Cursor):
                result = list(result)
            return result
        
        return wrapper