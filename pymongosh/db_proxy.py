from pymongo.cursor import Cursor

class DBProxy:
    def __init__(self, mongo_shell):
        self.mongo_shell = mongo_shell


    def __getattr__(self, name):
        if self.mongo_shell.db is None:
            raise Exception("No database selecte. Use 'use <database_name>' to select a database")
        
        # Handle database-level commands
        if name in ['addUser', 'createRole', 'dropUser', 'dropRole', 'grantRolesToUser', 'revokeRolesFromUser']:
            def command_method(*args):
                command = {name: args[0]} if args else {name: 1}
                return self.mongo_shell.db.command(command)
            return command_method
        
        if name == 'dropDatabase':
            self.is_db_command = True
            return self._drop_db
        
        return MethodProxy(self.mongo_shell.db, name)
    
    def _drop_db(self):
        try:
            return self.mongo_sehll.client.drop_database(self.mongo_shell.db.name)
        
        except Exception as e:
            return f'Error: {str(e)}'
    
class MethodProxy:
    def __init__(self, db, name):
        self.db = db
        self.collection = getattr(db, name)

    def __getattr__(self, name):
        # Proxy the method call on the collection
        method = getattr(self.collection, name)

        def wrapper(*args, **kwargs):
            # Execute the method
            result = method(*args, **kwargs)

            # Check return type and format if necessary
            if isinstance(result, Cursor):
                result = list(result)
            if result is None and name == 'drop':
                return {"ok", 1}
            return result
        
        return wrapper