"""Compile Queries."""
import os
import re
import ast
import time
import json
import glob
import tabulate
from pathlib import Path

from .utils import create_model_for_table
from .hash_index import HashIndex, read_hash_index

# Data Definition Language
ddl = ["create"]

# Data Manipulation Language
dml = ["select", "insert"]

# Wildcard
wild = ["*"]

# Data Query Language
dql = ["from", "where", "limit"]

"""
Sql Grammar

CREATE [DATABASE/ TABLE] [table_name / db_name]

SELECT [WILDCARD/ column_names] FROM [table_name]
WHERE column_name_1=<> [AND/OR] column_name2=<>
LIMIT [INTEGER]

INSERT INTO [table_name]([column_names]) VALUES([values])
"""

my_whole_db = {}


def create_table(table):
    my_whole_db[table.__tablename__] = []


class Person:
    __tablename__ = "person"

    def __init__(self):
        self.id = (int, 5)
        self.name = (str, 100)
        self.age = (int, 2)


p = Person()
dtypes = p.__dict__

create_table(p)


class ParseException(Exception):
    pass


def parse_tokens(tokens):
    if tokens:
        return tokens[0]
    else:
        raise ParseException("Could not parse the SQL query")


class QueryParser(object):
    """Parse Query into into keywords."""

    def __init__(self, query):
        super(QueryParser, self).__init__()
        self.query = query

    def _parse(self, tokens):
        stripped_token = tokens.strip()

        # meta commands
        # .t -> List all Tables
        if stripped_token in (".t"):
            return 'LIST_TABLES', tokens
        # .db -> Current Database
        if stripped_token in (".db"):
            return 'CURRENT_DATABASE', tokens

        if stripped_token.startswith("create"):
            tokens = re.findall(r"create\s+(table|database)\s+([a-zA-Z_]*)(.*\((.*?)\))?", tokens)
            object, name, _ , cols = parse_tokens(tokens)
            return "CREATE", (object, name, cols)

        # dml commands
        if stripped_token.startswith("insert"):
            # insert
            tokens = re.findall(
                r"insert\s+into\s+([a-zA-Z_]*).*\((.*?)\).*\s+values.*\((.*?)\)", tokens
            )
            tablename, cols, values = parse_tokens(tokens)
            return "INSERT", (tablename, cols, values)

        if stripped_token.startswith("select"):
            # select
            cols = tablename = filters = limit = None
            # Limit
            if "limit" in tokens:
                limit = int(parse_tokens(re.findall(r"limit\s+(\d*)", tokens)))
                tokens = tokens.split("limit")[0].strip()
            # Filters
            if "where" in tokens:
                filters = parse_tokens(re.findall(r"where\s+(.*)", tokens))
                tokens = tokens.split("where")[0].strip()
            # Tablename and Columns
            tokens = re.findall(r"select\s+(.*?)\s*from\s+(\w*)\s?", tokens)
            cols, tablename = parse_tokens(tokens)

            return "SELECT", (cols, tablename, filters, limit)

        else:
            return ParseException("Could not parse the SQL query")

    def parse(self):
        # Add space & lowercase
        tokens = self.query.center(3).lower()
        parsed_tokens = self._parse(tokens)
        return parsed_tokens

class QueryExecutor(object):
    """Execute the Parsed Query."""

    # Default Database
    DATABASE = ".yeet"
    Path(DATABASE).mkdir(parents=True, exist_ok=True)

    def __init__(self, query):
        super(QueryExecutor, self).__init__()
        self.query = query

    def run(self):
        start = time.time()
        result = None
        qp = QueryParser(self.query)
        operation, tokens = qp.parse()

        if operation == "CURRENT_DATABASE":
            result = f"Current Database: {QueryExecutor.DATABASE}"

        if operation == "LIST_TABLES":
            _tables = []
            for file in glob.glob('yeet/*meta.json'):
                _tables.append(file.split("/")[1].split("_")[0])
            result = f"Tables:\n{_tables}"

        if operation == "CREATE":
            _object, name, cols = tokens
            # create database
            if _object == "database":
                if not cols == '': # Database should not have values:
                    raise Exception("Cannot create database with value entries")
                else:
                    if os.path.exists(name):
                        raise Exception(f"Database {name} already exists switching")
                    else:
                        os.mkdir(name)
                    QueryExecutor.DATABASE = name
            # create table
            if _object == "table":
                table_field = {}
                split_cols = cols.split(",")
                for col in split_cols:
                    col = re.sub(' +', ' ', col) # remove extra space
                    col_args = col.split(" ")
                    colname = col_args[0]
                    dtype, maxlen = col_args[1].split(".")
                    if len(col_args) == 2:
                        table_field[colname] = (dtype, int(maxlen))
                    elif len(col_args) == 3:
                        table_field[colname] = (dtype, int(maxlen), "index")
                    else:
                        raise Exception("Invalid Params")
                table_meta = json.dumps(table_field)
                with open(f'{QueryExecutor.DATABASE}/{name}_meta.json', 'w') as f:
                    f.write(table_meta)

        if operation == "INSERT":
            tablename, cols, values = tokens
            with open(f'{QueryExecutor.DATABASE}/{tablename}_meta.json', 'r') as f:
                table_meta = json.loads(f.read())
            for key,value in table_meta.items():
                if len(value) == 3:
                    _index_col = key
            tablemodel = create_model_for_table(tablename, table_meta)
            values = dict(zip(cols.split(","), values.split(",")))
            for key, value in values.items():
                _type = table_meta[key][0]
                if _type == "int":
                    values[key] = int(values[key])
                if _type == "str":
                    values[key] = str(values[key])
            # Use Pydantic to validate the data
            tablemodel(**values)
            tableindex = HashIndex(
                QueryExecutor.DATABASE,
                tablename
            )
            tableindex.insert(values[_index_col], values)
        
        if operation == "SELECT":
            cols, tablename, filters, limit = tokens
            tableindex = read_hash_index(
                dbname = QueryExecutor.DATABASE,
                tablename = tablename
            )
            _index = 1
            dataset = []
            while True:
                row = tableindex.get(_index)
                if row == "<NAN>":
                    break
                dataset.append(ast.literal_eval(row))
                _index+=1
            result = tabulate.tabulate([x.values() for x in dataset], dataset[0].keys())
        end = time.time()
        return result, operation, end-start
