from .mongo_shell import MongoShell
from .shell import InteractiveShell

def main():
    uri = "mongodb://localhost:27017"
    mongo_shell = MongoShell(uri)
    shell = InteractiveShell(mongo_shell)
    shell.start()

if __name__ == '__main__':
    main()
