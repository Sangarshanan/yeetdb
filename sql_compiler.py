import re
import ast

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
INSERT INTO [table_name]([column_names]) VALUES([values])
"""

my_whole_db = {}


def create_table(name, dtypes):
    my_whole_db[name] = []


tablename = "person"
dtypes = {"id": (int, 5), "name": (str, 100), "age": (int, 2)}
create_table(tablename, dtypes)


class QueryCompiler(object):
    """QueryCompiler"""
    def __init__(self, query):
        super(QueryCompiler, self).__init__()
        self.query = query

    @staticmethod
    def tokenizer(query):
        tokens = [token.lower() for token in query.split(" ")]
        return tokens

    @staticmethod
    def insert_table(tablename, col_names, values):
        table = my_whole_db[tablename]
        row = []
        record = dict(zip(col_names, values))
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
    def select_table(tablename, cols="*", filters={}, limit=None):
        return my_whole_db[tablename]

    @staticmethod
    def inside_bracket(char, evaluate=True):
        inside_b = re.search(r'\(.*?\)', char)[0]
        if evaluate:
            exp = ast.literal_eval(inside_b)
        else:
            exp = inside_b[1:-1].split(',')
        return exp

    def parse(self, tokens):
        for token in tokens:
            # meta commands
            if token.startswith("."):
                if token[1:] == 't':
                    return '\n'.join(my_whole_db.keys())

            # dml commands
            if token in dml:
                # insert
                if token == 'insert':
                    tablename = tokens[2].split('(')[0]
                    cols = self.inside_bracket(tokens[2], evaluate=False)
                    values = self.inside_bracket(tokens[3])
                    return self.insert_table(tablename, cols, values)
                # select
                if token == 'select':
                    tablename = tokens[-1]
                    return self.select_table(tablename)

    def run(self):
        tokens = self.tokenizer(self.query)
        return self.parse(tokens)

"""
INSERT INTO person(id,age,name) VALUES(1,25,'tyler')
SELECT * from person
"""
# q = QueryCompiler("INSERT INTO person(id,age,name) VALUES(1,25,'tyler')")
# print(q.run())
