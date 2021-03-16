"""Compile Queries."""
import re

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
            return tokens

        if stripped_token.startswith("create"):
            tokens = re.findall(r"create\s+(table|database)\s+([a-zA-Z_]*)", tokens)
            object, name = parse_tokens(tokens)
            return object, name

        # dml commands
        if stripped_token.startswith("insert"):
            # insert
            tokens = re.findall(
                r"insert\s+into\s+([a-zA-Z_]*).*\((.*?)\).*\s+values.*\((.*?)\)", tokens
            )
            tablename, cols, values = parse_tokens(tokens)
            return tablename, cols, values

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

            return cols, tablename, filters, limit

        else:
            return ParseException("Could not parse the SQL query")

    def parse(self):
        # Add space & lowercase
        tokens = self.query.center(3).lower()
        return self._parse(tokens)
