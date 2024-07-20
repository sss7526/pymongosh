import unittest
from unittest.mock import MagicMock
import mongomock
from pymongosh.mongo_shell import MongoShell
from pymongosh.db_proxy import DBProxy
import json

class TestDBProxy(unittest.TestCase):
    def setUp(self):
        # Use mongomock to simulate MongoDB
        self.client = mongomock.MongoClient()
        self.mongo_shell = MongoShell('mongodb://localhost:27017')
        self.mongo_shell.client = self.client
        self.db_proxy = DBProxy(self.mongo_shell)
        self.mongo_shell.use_database('testdb')

    def test_add_user(self):
        result = self.db_proxy.addUser('testUser', 'password123', [{"role": "readWrite", "db": "testdb"}])
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
        self.assertTrue(result.get("ok"), 1.0)

    def test_drop_user(self):
        self.db_proxy.addUser('testUser', 'password123', [{"role": "readWrite", "db": "testdb"}])
        result = self.db_proxy.dropUser('testUser')
        self.assertTrue(result.get("ok"), 1.0)

    def test_drop_role(self):
        role_def = {
            "createRole": "testRole",
            "privileges": [{
                "resource": {"db": "testdb", "collection": ""},
                "actions": ["find"]
            }],
            "roles": []
        }
        self.db_proxy.createRole(role_def)
        result = self.db_proxy.dropRole('testRole')
        self.assertTrue(result.get("ok"), 1.0)

    def test_grant_roles_to_user(self):
        self.db_proxy.addUser('testUser', 'password123', [])
        result = self.db_proxy.grantRolesToUser('testUser', [{"role": "readWrite", "db": "testdb"}])
        self.assertTrue(result.get("ok"), 1.0)

    def test_revoke_roles_from_user(self):
        self.db_proxy.addUser('testUser', 'password123', [{"role": "readWrite", "db": "testdb"}])
        result = self.db_proxy.revokeRolesFromUser('testUser', [{"role": "readWrite", "db": "testdb"}])
        self.assertTrue(result.get("ok"), 1.0)

    def test_get_user(self):
        self.db_proxy.addUser('testUser', 'password123', [{"role": "readWrite", "db": "testdb"}])
        result = self.db_proxy.getUser('testUser')
        self.assertTrue(result.get("ok"), 1.0)
        self.assertEqual(result['users'][0]['user'], 'testUser')

    def test_drop_database(self):
        result = self.db_proxy.dropDatabase()
        self.assertTrue(result.get("ok"), 1.0)

if __name__ == '__main__':
    unittest.main()