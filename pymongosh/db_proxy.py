from pymongo.cursor import Cursor

class DBProxy:
    def __init__(self, mongo_shell):
        self.mongo_shell = mongo_shell


    def __getattr__(self, name):
        if self.mongo_shell.db is None:
            raise Exception("No database selecte. Use 'use <database_name>' to select a database")
        
        # Handle database-level commands
        if name in ['addUser', 'createRole', 'dropUser', 'dropRole', 'grantRolesToUser', 'revokeRolesFromUser', 'getUser', 'dropDatabase']:
            return getattr(self, name)
        
        return MethodProxy(self.mongo_shell.db, name)
    
    def addUser(self, *args, **kwargs):
        try:
            return self.mongo_shell.db.add_user(*args, **kwargs)
        except Exception as e:
            return f'Error: {str(e)}'
        
    def createRole(self, *args, **kwargs):
        try:
            return self.mongo_shell.db.command('createRole', *args, **kwargs)
        except Exception as e:
            return f'Error: {str(e)}'
        
    def dropUser(self, *args, **kwargs):
        try:
            return self.mongo_shell.db.command('dropUser', *args, **kwargs)
        except Exception as e:
            return f'Error: {str(e)}'
        
    def dropRole(self, *args, **kwargs):
        try:
            return self.mongo_shell.db.command('dropRole', *args, **kwargs)
        except Exception as e:
            return f'Error: {str(e)}'
        
    def grandRolesToUser(self, user, roles):
        try:
            return self.mongo_shell.db.command('grantRolesToUser', user=user, roles=roles)
        except Exception as e:
            return f'Error: {str(e)}'
        
    def revokeRolesFromUser(self, user, roles):
        try:
            return self.mongo_shell.db.command('revokeRolesFromUser', user=user, roles=roles)
        except Exception as e:
            return f'Error: {str(e)}'
        
    def getUser(self, user):
        try:
            return self.mongo_shell.db.command('usersInfo', {'user': user})
        except Exception as e:
            return f'Error: {str(e)}'

    def dropDatabase(self, *args, **kwargs):
        try:
            return self.mongo_shell.client.drop_database(self.mongo_shell.db.name)
        
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