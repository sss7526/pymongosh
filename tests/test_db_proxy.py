import unittest
from pymongo import MongoClient
from pymongosh.mongo_shell import MongoShell
from pymongosh.db_proxy import DBProxy
import json

class TestDBProxy(unittest.TestCase):
    def setUp(self):
        # Connect to a real MongoDB instance
        uri = "mongodb://localhost:27017"
        self.client = MongoClient(uri)
        
        # Drop the test database if it exists to ensure a clean state
        self.client.drop_database('testdb')
        
        self.mongo_shell = MongoShell(uri)
        self.db_proxy = DBProxy(self.mongo_shell)
        self.mongo_shell.use_database('testdb')

        try:
            self.db_proxy.dropUser('testUser')
        except:
            pass

    def tearDown(self):
        self.client.drop_database('testdb')

    def test_add_user(self):
        result = self.db_proxy.addUser('testUser', 'password123', [{"role": "readWrite", "db": "testdb"}])
        if result.get("ok") != 1.0:
            print(f'Failed to add user: {result}')
        self.assertEqual(result.get("ok"), 1.0)
    
    def test_create_role(self):
        role_def = {
            "createRole": "testRole",
            "privileges": [{
                "resource": {"db": "testdb", "collection": ""},
                "actions": ["find"]
            }],
            "roles": []
        }
        result = self.db_proxy.createRole(role_def)
        self.assertEqual(result.get("ok"), 1.0)

    def test_drop_user(self):
        self.db_proxy.addUser('testUser', 'password123', [{"role": "readWrite", "db": "testdb"}])
        result = self.db_proxy.dropUser('testUser')
        self.assertEqual(result.get("ok"), 1.0)

    def test_drop_role(self):
        role_def = {
            "createRole": "testRole",
            "privileges": [{
                "resource": {"db": "testdb", "collection": ""},
                "actions": ["find"]
            }],
            "roles": []
        }
        command = {'createRole': 'testRole', 'privileges': role_def['privileges'], 'roles': role_def['roles']}
        self.db_proxy.createRole(command)
        result = self.db_proxy.dropRole('testRole')
        self.assertEqual(result.get("ok"), 1.0)

    def test_grant_roles_to_user(self):
        self.db_proxy.addUser('testUser', 'password123', [])
        result = self.db_proxy.grantRolesToUser('testUser', [{"role": "readWrite", "db": "testdb"}])
        self.assertEqual(result.get("ok"), 1.0)

    def test_revoke_roles_from_user(self):
        self.db_proxy.addUser('testUser', 'password123', [{"role": "readWrite", "db": "testdb"}])
        result = self.db_proxy.revokeRolesFromUser('testUser', [{"role": "readWrite", "db": "testdb"}])
        self.assertEqual(result.get("ok"), 1.0)

    def test_get_user(self):
        self.db_proxy.addUser('testUser', 'password123', [{"role": "readWrite", "db": "testdb"}])
        result = self.db_proxy.getUser('testUser')
        self.assertEqual(result.get("ok"), 1.0)
        self.assertEqual(result['users'][0]['user'], 'testUser')

    def test_drop_database(self):
        result = self.db_proxy.dropDatabase()
        self.assertEqual(result.get("ok"), 1.0)

if __name__ == '__main__':
    unittest.main()