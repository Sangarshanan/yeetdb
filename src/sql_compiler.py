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


class QueryCompiler(object):
    """QueryCompiler"""

    def __init__(self, query):
        super(QueryCompiler, self).__init__()
        self.query = query

    @staticmethod
    def tokenizer(query):
        query = re.sub(' +', ' ', query)
        tokens = [token.lower() for token in query.split(" ")]
        return tokens

    @staticmethod
    def inside_bracket(char, evaluate=True):
        inside_b = re.search(r"\(.*?\)", char)[0]
        if evaluate:
            exp = ast.literal_eval(inside_b)
        else:
            exp = inside_b[1:-1].split(",")
        return exp

    def insert_parser(self, tokens):
        tablename = tokens[2].split("(")[0]
        cols = self.inside_bracket(tokens[2], evaluate=False)
        values = self.inside_bracket(tokens[3])
        return tablename, cols, values

    @staticmethod
    def insert(tablename, col_names, values):
        table = my_whole_db[tablename]
        row = []
        record = OrderedDict(zip(col_names, values))
        for key in sorted(record.keys(), key=lambda x: x.lower()):
            value = record[key]
            # dtype is maintained
            assert type(value) == dtypes[key][0]
            # length is maintained
            assert len(str(value)) <= dtypes[key][1]
            row.append(value)
        table.append(row)
        return f"INSERT {values}"

    @staticmethod
    def select_parser(tokens):
        tablename = tokens[tokens.index('from')+1]

        # Columns
        if tokens[1] == '*':
            # Wildcard
            cols = None
        else:
            raw_cols = tokens[1:tokens.index('from')]
            cols = [c.replace(',','') for c in raw_cols]

        # Limit
        if 'limit' in tokens:
            limit = int(tokens[-1])
            end_of_query = tokens.index('limit')
        else:
            limit = None

        # Filters
        if 'where' in tokens:
            if limit is None:
                filters = tokens[tokens.index('where')+1:]
            else:
                filters = tokens[tokens.index('where')+1:end_of_query]
            pd_query = ' '.join(filters).replace('=','==')
            filters = pd_query
        else:
            filters = None

        return tablename, cols, filters, limit

    @staticmethod
    def select(tablename, cols, filters, limit):
        if my_whole_db[tablename]:
            df = pandas.DataFrame(my_whole_db[tablename], columns=sorted(dtypes.keys()))
            if filters:
                df = df.query(filters).reset_index(drop=True)
            if limit:
                df = df.sample(limit).reset_index(drop=True)
            if cols:
                df = df[cols]
        else:
            df = "EMPTY"
        return df

    def parse(self, tokens):
        for token in tokens:
            # meta commands
            if token.startswith("."):
                if token[1:] == "t":
                    return "\n".join(my_whole_db.keys())

            # dml commands
            if token in dml:
                # insert
                if token == "insert":
                    tablename, cols, values = self.insert_parser(tokens)
                    return self.insert(tablename, cols, values)
                # select
                if token == "select":
                    tablename, cols, filters, limit = self.select_parser(tokens)
                    return self.select(tablename, cols, filters, limit)

    def run(self):
        tokens = self.tokenizer(self.query)
        return self.parse(tokens)
