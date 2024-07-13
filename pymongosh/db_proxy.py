class DBProxy:
    def __init__(self, mongo_shell):
        self.mongo_shell = mongo_shell

    def __getattr__(self, name):
        if self.mongo_shell.db is None:
            raise Exception("No database selecte. Use 'use <database_name>' to select a database")
        
        collection = getattr(self.mongo_shell.db, name)
        if collection is not None:
            return MethodProxy(collection)
        raise AttributeError(f"'DBProxy' ojbect has not attribute '{name}'")
    
class MethodProxy:
    def __init__(self, collection):
        self.collection = collection

    def __getattr__(self, name):
        method = getattr(self.collection, name)

        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        
        return wrapper