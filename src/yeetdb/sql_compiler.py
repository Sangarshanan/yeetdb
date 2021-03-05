import re
import ast
import pandas
from collections import OrderedDict

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
    __tablename__ = 'person'
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
        start_token = tokens[0]

        stripped_token = tokens.strip()
        # meta commands
        if stripped_token == ".t":
            # All tablenames
            print("Table names")
            return "\n".join(my_whole_db.keys())

        # dml commands
        if tokens.startswith("insert"):
            # insert
            tablename, cols, values = self.insert_parser(tokens)
            return self.insert(tablename, cols, values)

        if tokens.startswith("select"):
            # select
            tokens = re.findall(
                r'select\s+(.*?)\s*from\s+(\w*)\s?(where?\s+(.*))?\s?(limit?\s(\d*))?', tokens)
            cols,tablename,_,filters,_,limit = parse_tokens(tokens)
            return cols, tablename, filters, limit

    def parse(self):
         # Add space & lowercase
        tokens = self.query.center(3).lower()
        return self._parse(tokens)
