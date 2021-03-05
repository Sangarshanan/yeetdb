from yeetdb.sql_compiler import QueryParser

qc = QueryParser("""SELECT a,b,c
FROM tablename
where a>10 and b <20
limit 10
"""
)
print(qc.parse())
assert ('a,b,c', 'tablename', 'a>10 and b <20', '10') == qc.parse()

qc = QueryParser("SELECT * from monki")
print(qc.parse())
assert ('*', 'monki', '', '') == qc.parse()


qc = QueryParser("SELECT a,b from test where x>10")
print(qc.parse())
assert ('a,b', 'test', 'x>10', '') == qc.parse()


qc = QueryParser("SELECT * from test limit 200")
print(qc.parse())
assert ('*', 'test', '', '200') == qc.parse()
