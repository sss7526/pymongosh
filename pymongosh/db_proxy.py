from .method_proxy import MethodProxy

class DBProxy:
    def __init__(self, mongo_shell):
        self.mongo_shell = mongo_shell

    def __getattr__(self, name):
        if self.mongo_shell.db is None:
            raise Exception("No database selected. Use 'use <database_name>' to select a database")
        
        # Handle database-level commands
        if name in ['addUser', 'createRole', 'dropUser', 'dropRole', 'grantRolesToUser', 'revokeRolesFromUser', 'getUser', 'dropDatabase']:
            return getattr(self, name)
        
        return MethodProxy(self.mongo_shell.db, name)

    def addUser(self, username, password, roles):
        try:
            # Construct the command properly
            command = {
                "createUser": username,
                "pwd": password,
                "roles": roles
            }
            result = self.mongo_shell.db.command(command)
            return result
        except Exception as e:
            return {"ok": 0, "error": str(e)}
        
    def createRole(self, role_def):
        try:
            return self.mongo_shell.db.command(role_def)
        except Exception as e:
            return {"ok": 0, "error": str(e)}
        
    def dropUser(self, username):
        try:
            return self.mongo_shell.db.command('dropUser', username)
        except Exception as e:
            return {"ok": 0, "error": str(e)}
        
    def dropRole(self, role_name):
        try:
            return self.mongo_shell.db.command('dropRole', role_name)
        except Exception as e:
            return {"ok": 0, "error": str(e)}
        
    def grantRolesToUser(self, user, roles):
        try:
            command = {
                'grantRolesToUser': user,
                'roles':roles
            }
            return self.mongo_shell.db.command(command)
        except Exception as e:
            return {"ok": 0, "error": str(e)}
        
    def revokeRolesFromUser(self, user, roles):
        try:
            command = {
                'revokeRolesFromUser': user,
                'roles': roles
            }
            return self.mongo_shell.db.command(command)
        except Exception as e:
            return {"ok": 0, "error": str(e)}
        
    def getUser(self, username):
        try:
            return self.mongo_shell.db.command('usersInfo', {'user': username, 'db': self.mongo_shell.db.name})
        except Exception as e:
            return {"ok": 0, "error": str(e)}

    def dropDatabase(self, *args, **kwargs):
        try:
            self.mongo_shell.client.drop_database(self.mongo_shell.db.name)
            return {"ok":1}
        except Exception as e:
            return {"ok": 0, "error": str(e)}
        
    def runCommand(self, command):
        try:
            result = self.mongo_shell.db.command(command)
            return result
        except Exception as e:
            return {"ok":0, "error": str(e)}