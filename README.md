# pymongosh

**pymongosh** is a simple interactive shell for working with MongoDB, implemented in Python. If you find yourself needing to administer databases but don't have access to Compass or mongosh (for whatever ridiculous reason), this tool is for you.

## Features

- List databases
- Use a specific database
- List collections in the selected database
- Execute queries on collections
- Run MongoDB commands
- Insert documents into collections
- Drop databases and collections
- Use db alias commands that emulate mongosh command syntax
- Supports multi-line input like mongosh
- Includes command auto-completion

## Requirements

- Python 3.x
- MongoDB

## Installation

Clone the repository:
```sh
git clone https://github.com/sss7526/pymongosh.git
cd pymongosh
```

Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate    # On Windows, use `venv\Scripts\activate`
```

Install the dependencies:
```sh
pip install -r requirements.txt
```

## Usage

Ensure your MongoDB instance is running.

Run the interactive shell:
```sh
python -m pymongosh
```


### list_databases

List all databases.
```sh
mongo-shell> list_databases
['admin', 'local', 'test']
```

### use

Switch to a specific database.
```sh
mongo-shell> use mydatabase
Using database: mydatabase
```

### list_collections

List all collections in the current database.
```sh
mongo-shell> list_collections
['collection1', 'collection2']
```

### query

Execute a query on a collection.
```sh
mongo-shell> query mycollection {"field": "value"}
[{'_id': ObjectId('...'), 'field': 'value'}]
```

### command

Execute a MongoDB command.
```sh
mongo-shell> command {"ping": 1}
{'ok': 1.0}
```

### insert

Insert a document into a collection.
```sh
mongo-shell> insert mycollection {"field": "value"}
{'_id': 'ObjectId("...")'}
```

### drop_database

Drop a specified database.
```sh
mongo-shell> drop_database mydatabase
Database mydatabase dropped
```

### drop_collection

Drop a specified collection.
```sh
mongo-shell> drop_collection mycollection
Collection mycollection dropped
```

### help

Show this help prompt.
```sh
mongo-shell> help
Available commands:
  list_databases                                Lists all databases.
  use <database_name>                           Switches to the specified database.
  list_collections                              Lists all collections in the current database.
  query <collection_name> <query_json>          Executes a query on the specified collection. Use JSON format for the query.
  command <command_json>                        Executes a JSON command on the current database.
  insert <collection_name> <document_json>      Inserts a document into the specified collection. Use JSON format for the document.
  drop_database <database_name>                 Drops the specified database.
  drop_collection <collection_name>             Drops the specified collection.
  help                                          Displays this help message.
  exit                                          Exits the MongoDB shell.

Using the db alias:
  db.<collection_name>.<method>(<args>)         Executes a MongoDB method on the specified collection.
  db.<command>(<args>)                          Executes a MongoDB database command.

For detailed usage examples, visit: https://github.com/sss7526/pymongosh
```

### exit

Exit the shell.
```sh
mongo-shell> exit
Exiting pymongosh...
```

## Usage Examples for `db` Alias Commands

The following include a set of usage examples for the `db` alias commands at both the database and collection levels. These examples emulate typical `mongosh` usage.

### Database-Level Commands

1. **addUser()**

    Adds a new user with specified roles to the database.
    ```python
    mongo-shell> db.createUser("username", "password", [{"role": "readWrite", "db": "testdb"}])
    ```

2. **dropUser()**

    Drops a user from the database.
    ```python
    mongo-shell> db.dropUser("username")
    ```


3. **createRole()**

    Creates a custom role in the database.
    ```python
    mongo-shell> db.createRole({
        "role": "myCustomRole",
        "privileges": [{"resource": {"db": "testdb", "collection": ""}, "actions": ["find", "update"]}],
        "roles": []
    })
    ```

4. **dropRole()**

    Drops a custom role from the database.
    ```python
    mongo-shell> db.dropRole("myCustomRole")
    ```

5. **grantRolesToUser()**

    Grants roles to a user.
    ```python
    mongo-shell> db.grantRolesToUser("username", [{"role": "readWrite", "db": "testdb"}])
    ```

6. **revokeRolesFromUser()**

    Revokes roles from a user.
    ```python
    mongo-shell> db.revokeRolesFromUser("username", [{"role": "readWrite", "db": "testdb"}])
    ```

7. **getUser()**
    Retrieves information about a user.
    ```python
    mongo-shell> db.getUser("username")
    ```

8. **dropDatabase()**

    Drops the current database.
    ```python
    mongo-shell> db.dropDatabase()
    ```

9. **runCommand()**

    Executes any given MongoDB command on the database.
    ```python
    mongo-shell> db.runCommand({"ping": 1})
    ```

### Collection-Level Commands

1. **insertOne()**

    Inserts a single document into the collection.
    ```python
    mongo-shell> db.myCollection.insertOne({"name": "John", "age": 30})
    ```

2. **findOne()**

    Finds a single document that matches the query criteria.
    ```python
    mongo-shell> db.myCollection.findOne({"name": "John"})
    ```

3. **deleteOne()**

    Deletes the first document that matches the query criteria.
    ```python
    mongo-shell> db.myCollection.deleteOne({"name": "John"})
    ```

4. **updateOne()**

    Updates the first document that matches the query criteria.
    ```python
    mongo-shell> db.myCollection.updateOne({"name": "John"}, {"$set": {"age": 31}})
    ```

5. **replaceOne()**

    Replaces the first document that matches the query criteria.
    ```python
    mongo-shell> db.myCollection.replaceOne({"name": "John"}, {"name": "John", "age": 32})
    ```

6. **insertMany()**

    Inserts multiple documents into the collection.
    ```python
    mongo-shell> db.myCollection.insertMany([{"name": "Alice", "age": 25}, {"name": "Bob", "age": 27}])
    ```

7. **deleteMany()**

    Deletes all documents that match the query criteria.
    ```python
    mongo-shell> db.myCollection.deleteMany({"age": {"$lt": 30}})
    ```

8. **drop()**

    Drops the specified collection.
    ```python
    mongo-shell> db.myCollection.drop()
    ```
