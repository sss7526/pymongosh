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
    parser.add_argument("--authenticationDatabase", type=str, help="Database to authenticate against")
    parser.add_argument("--authenticationMechanism", type=str, help="Authentication mechanism to use")

    parser.add_argument("--tls", action="store_true", help="Use TLS/SSL when connecting to MongoDB")

    args = parser.parse_args()
    return args

def main():
    args = parse_the_args()

    if args.uri:
        uri = args.uri
    else:
        host = args.host
        port = args.port
        query_params = {}

        if args.username and args.password:
            username = urllib.parse.quote_plus(args.username)
            password = urllib.parse.quote_plus(args.password)
            credentials = f'{username}:{password}@'

            if args.authenticationDatabase:
                query_params['authSource'] = args.authenticationDatabase
            else:
                query_params['authSource'] = 'admin'

            if args.authenticationMechanism:
                query_params['authMechanism'] = args.authenticationMechanism
            else:
                query_params['authMechanism'] = 'SCRAM-SHA-256'

            uri = f'mongodb://{credentials}{host}:{port}'
        else:
            uri = f'mongodb://{host}:{port}'

        if args.tls:
            query_params['tls'] = 'true'

        if query_params:
            uri += "?" + '&'.join(f'{key}={value}' for key, value in query_params.items())

    mongo_shell = MongoShell(uri)
    shell = InteractiveShell(mongo_shell)
    shell.start()

if __name__ == '__main__':
    main()
