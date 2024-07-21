import argparse
import urllib.parse
from .mongo_shell import MongoShell
from .shell import InteractiveShell

def parse_the_args():
    parser = argparse.ArgumentParser(description="A MongoDB CLI tool to emulate mongosh (because of reasons)")

    # positional argument for MongoDB URI
    parser.add_argument("uri", nargs='?', help="MongoDB URI")
    
    # Optional arguments for host and port
    parser.add_argument("--host", type=str, default='localhost', help="MongoDB host")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB port (default 27017)")
    
    parser.add_argument("-u", "--username", type=str, help="MongoDB username")
    parser.add_argument("-p", "--password", type=str, help="MongoDB password")

    args = parser.parse_args()
    return args

def main():
    args = parse_the_args()

    if args.uri:
        uri = args.uri
    else:
        host = args.host
        port = args.port
        if args.username and args.password:
            username = urllib.parse.quote_plus(args.username)
            password = urllib.parse.quote_plus(args.password)
            uri = f'mongodb://{username}:{password}@{host}:{port}'
        else:
            uri = f'mongodb://{host}:{port}'

    mongo_shell = MongoShell(uri)
    shell = InteractiveShell(mongo_shell)
    shell.start()

if __name__ == '__main__':
    main()
