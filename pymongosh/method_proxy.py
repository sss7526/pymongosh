from pymongo.cursor import Cursor

class MethodProxy:
    def __init__(self, db, name):
        self.db = db
        self.collection = getattr(db, name)

    def __getattr__(self, name):
        # Translate mongosh method names to pymongo method names
        method_name = self.translate_mongosh_method(name)
        method = getattr(self.collection, method_name)

        def wrapper(*args, **kwargs):
            try:
                # Execute the method
                result = method(*args, **kwargs)

                # Check return type and format if necessary
                if isinstance(result, Cursor):
                    result = list(result)
                if result is None and name == 'drop':
                    return {"ok": 1}
                return result
            except Exception as e:
                return f'Error: {str(e)}'
        
        return wrapper

    def translate_mongosh_method(self, name):
        translations = {
            'findOne': 'find_one',
            'insertOne': 'insert_one',
            'deleteOne': 'delete_one',
            'updateOne': 'update_one',
            'replaceOne': 'replace_one',
            'insertMany': 'insert_many',
            'deleteMany': 'delete_many'
            # Add more translations as necessary
        }
        return translations.get(name, name)  # Fallback to the original name if no translation is found