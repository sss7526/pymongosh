from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout
from pymongo.errors import PyMongoError
import json
from .custom_json_encoder import MongoJSONEncoder
from .db_proxy import DBProxy

class InteractiveShell:
    def __init__(self, mongo_shell):
        self.mongo_shell = mongo_shell
        self.db = DBProxy(mongo_shell)
        self.session = PromptSession()
        self.commands = WordCompleter([
            'list_databases', 
            'use', 
            'list_collections', 
            'query', 
            'command',
            'exit',
            'help'
        ], ignore_case=True)

    def start(self):
        print("When you're given a spoon to dig a trench, build your own shovel\nType 'help' to list available commands.")
        while True:

            try:
                with patch_stdout():
                    #user_input = self.session.prompt('mongo-shell>', completer=self.commands, complete_while_typing=True).strip()
                    user_input = self.read_command()

                if not user_input:
                    continue
                
                if user_input.startswith('db.'):
                    result = self.process_db_commands(user_input)
                    print(result)
                
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
                            print("Invalid query format. Use: 'query <collection_name> <query_json>'")
                            continue

                        collection, query = coll_query

                        try:
                            query_json = json.loads(query)
                            result = self.mongo_shell.execute_query(collection, query_json)
                            print(self.format_output(result))

                        except json.JSONDecodeError as e:
                            print(f'Invalid JSON format: {str(e)}')

                    elif command == 'command':

                        try:
                            command_json = json.loads(args)
                            result = self.mongo_shell.execute_command(command_json)
                            print(self.format_output(result))

                        except json.JSONDecodeError as e:
                            print(f'Invalid JSON format: {str(e)}')
                    
                    elif command == 'insert':
                        coll_doc = args.split(' ', 1)
                        if len(coll_doc) != 2:
                            print('Invalid insert format, Use: insert <collection_name> <document_json>')
                            continue

                        collection, document = coll_doc
                        result = self.mongo_shell.insert_document(collection, document)
                        print(self.format_output(result))

                    elif command == 'help':
                        self.display_help()

                    elif command == 'exit':
                        print('Exiting Mongo Shell. Goodbye!')
                        break

                    else:
                        print(f'Unknown command: {command}')
            
            except KeyboardInterrupt:
                print("Use 'Ctrl+D' to kill the shell if that's what you want.")
                continue # Ctrl+C pressed

            except EOFError:
                break # Ctrl+D pressed

            except Exception as e:
                print(f'Error: {str(e)}')

        self.mongo_shell.close()

    def format_output(self, output):
        if isinstance(output, (list, dict)):
            return json.dumps(output, indent=4, cls=MongoJSONEncoder)
        
        return str(output)
    
    def process_db_commands(self, command):
        command = command[3:]
        collection_name, method_call = command.split('.', 1)
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
            prompt = 'mongo_shell> ' if not multiline_input else '... '
            user_input = self.session.prompt(prompt, completer=self.commands)
            multiline_input += user_input + '\n'
            
            if self.is_complete(multiline_input):
                break
        
        return multiline_input.strip()
    
    def is_complete(self, text):
        # command is considered complete if the number of opening brackets matches the number of closing brackets
        if (text.count('(') == text.count(')') and 
            text.count('{') == text.count('}') and 
            text.count('[') == text.count(']')):
            return True
        return False

    def display_help(self):
        help_message = """
Availabale Commands:
    list_databases                      Lists all databases
    use <database_name>                 Switches to the specified database
    list_collections                    Lists all collections in the current database
    query <collection> <query_json>     Executes a query on the specified collection. Use JSON format for the query.
    command <command_json>              Executes a JSON command on the current database.
    insert <collection> <document_json> Inserts a document into the specified collection. Use JSON format for the document.
    help                                Displays this help message.
    exit                                Exits the MongoDB shell.
    
Examples:
    use mydatabase
    list_collections
    query mycollection {"field": "value"}
    command {"ping": 1}
    insert mycollection {"field": "value"}
        """
        print(help_message)
