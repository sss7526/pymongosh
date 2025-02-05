from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout
import json
import pymongo
from .custom_json_encoder import MongoJSONEncoder
from .mongo_shell import MongoShell
from .db_proxy import DBProxy

class InteractiveShell:
    def __init__(self, mongo_shell):
        self.mongo_shell = mongo_shell
        self.db = DBProxy(mongo_shell)
        self.session = PromptSession()
        self.commands = WordCompleter([
            'list_databases', 'use', 'list_collections', 'query', 'command', 'insert', 
            'drop_database', 'drop_collection', 'help', 'exit'
        ], ignore_case=True)

    def start(self):
        print("Welcome to pymongosh! Type 'help' to list available commands.")
        while True:
            try:
                with patch_stdout():
                    user_input = self.read_command()
                
                if not user_input:
                    continue

                if user_input.startswith('db.'):
                    result = self.process_db_commands(user_input)
                    print(self.format_output(result))
                else:
                    command_components = user_input.split(' ', 1)
                    command = command_components[0]
                    args = command_components[1] if len(command_components) > 1 else ''

                    if command == 'list_databases':
                        result = self.mongo_shell.list_databases()
                        print(self.format_output(result))
                    elif command == 'use':
                        result = self.mongo_shell.use_database(args)
                        print(result)
                    elif command == 'list_collections':
                        result = self.mongo_shell.list_collections()
                        print(self.format_output(result))
                    elif command == 'query':
                        coll_query = args.split(' ', 1)
                        if len(coll_query) != 2:
                            print("Invalid query format. Use: query <collection_name> <query_json>")
                            continue
                        collection, query = coll_query
                        try:
                            query_json = json.loads(query)
                            result = self.mongo_shell.execute_query(collection, query_json)
                            print(self.format_output(result))
                        except json.JSONDecodeError as e:
                            print(f"Invalid JSON format: {str(e)}")
                    elif command == 'command':
                        try:
                            command_json = json.loads(args)
                            result = self.mongo_shell.execute_command(command_json)
                            print(self.format_output(result))
                        except json.JSONDecodeError as e:
                            print(f"Invalid JSON format: {str(e)}")
                    elif command == 'insert':
                        coll_doc = args.split(' ', 1)
                        if len(coll_doc) != 2:
                            print("Invalid insert format. Use: insert <collection_name> <document_json>")
                            continue
                        collection, document = coll_doc
                        result = self.mongo_shell.insert_document(collection, document)
                        print(self.format_output(result))
                    elif command == 'drop_database':
                        result = self.drop_database(args)
                        print(self.format_output(result))
                    elif command == 'drop_collection':
                        result = self.drop_collection(args)
                        print(self.format_output(result))
                    elif command == 'help':
                        self.display_help()
                    elif command == 'exit':
                        print("Exiting Mongo Shell. Goodbye!")
                        break
                    else:
                        print(f"Unknown command: {command}")

            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D pressed.
            except Exception as e:
                print(f"Error: {str(e)}")

        self.mongo_shell.close()

    def format_output(self, output):
        if isinstance(output, (list, dict)):
            return json.dumps(output, indent=4, cls=MongoJSONEncoder)
        return str(output)

    def process_db_commands(self, command):
        command = command[3:]  # Remove the `db.` part
        parts = command.split('.', 1)
        if len(parts) == 1:
            method_name, args_json = parts[0].split('(', 1)
            args_json = args_json.rstrip(')')
            args = json.loads('[' + args_json + ']')
            method = getattr(self.db, method_name)
            result = method(*args)
        else:
            collection_name, method_call = parts
            method_name, args_json = method_call.split('(', 1)
            args_json = args_json.rstrip(')')
            args = json.loads('[' + args_json + ']')
            collection = getattr(self.db, collection_name)
            method = getattr(collection, method_name)
            result = method(*args)
        return result

    def read_command(self):
        multiline_input = ""
        while True:
            if self.mongo_shell.db is not None:
                prompt = f'mongo-shell [{self.mongo_shell.db.name}]> ' if not multiline_input else '... '
            else:
                prompt = 'mongo-shell [No DB]> ' if not multiline_input else '... '
            user_input = self.session.prompt(prompt, completer=self.commands)
            multiline_input += user_input + "\n"
            if self.is_complete(multiline_input):
                break
        return multiline_input.strip()
    
    def is_complete(self, text):
        # A command is considered complete if the number of opening brackets matches the number of closing brackets.
        if text.count('(') == text.count(')') and text.count('{') == text.count('}') and text.count('[') == text.count(']'):
            return True
        return False

    def drop_database(self, db_name):
        try:
            self.mongo_shell.client.drop_database(db_name)
            return {"ok": 1}
        except Exception as e:
            return {"error": str(e)}

    def drop_collection(self, collection_name):
        if self.mongo_shell.db is None:
            return {"error": "No database selected. Use 'use <database_name>' to select a database."}

        if collection_name not in self.mongo_shell.db.list_collection_names():
            return {"error": f"Collection '{collection_name}' does not exist."}
        
        try:
            self.mongo_shell.db.drop_collection(collection_name)
            return {"ok": 1}
        except Exception as e:
            return {"error": str(e)}

    def display_help(self):
        help_message = """
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
        """
        print(help_message)