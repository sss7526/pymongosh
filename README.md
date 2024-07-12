# pymongosh
python implementation of mongosh for when you don't have what you need.

`pymongosh` is a simple interactive shell for working with MongoDB, implemented in Python, if for whatever reason you find yourself needing to administer databases but don't have access to Compass or mongosh

## Features
- List databases
- Use a specific database
- List collections in the selected database
- Execute queries on collections
- Run MongoDB commands
- Insert documents into collections

## Requirements

- Python 3.x
- MongoDB

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sss7526/pymongosh.git
    cd pymongosh
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate    # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Ensure your MongoDB instance is running.

2. Run the interactive shell:
    ```sh
    python -m pymongosh
    ```

3. In the shell, you can use the following commands:
    - `list_databases`: List all databases.
    - `use <database_name>`: Switch to a database.
    - `list_collections`: List all collections in the current database.
    - `query <collection_name> <query_json>`: Execute a query on a collection.
    - `command <command_json>`: Execute a MongoDB command.
    - `insert <collection_name> <document_json>`: Insert a document into a collection.
    - `exit`: Exit the shell.
    - `help`: Show help prompt
