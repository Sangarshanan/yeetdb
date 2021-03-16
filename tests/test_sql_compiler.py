from yeetdb.sql_compiler import QueryParser


class TestQueryParserSelect:
    def test_query_parser_select_simple(self):
        # Simple
        qc = QueryParser("SELECT * from monki")
        assert ("*", "monki", None, None) == qc.parse()

    def test_query_parser_select_filters(self):
        # Filters
        qc = QueryParser("SELECT a,b from test where x>10")
        assert ("a,b", "test", "x>10", None) == qc.parse()

    def test_query_parser_select_limit(self):
        # Limit
        qc = QueryParser("SELECT * from test limit 200")
        assert ("*", "test", None, 200) == qc.parse()

    def test_query_parser_select_filters_limit(self):
        # Filters and Limit
        qc = QueryParser("SELECT a,b,c FROM tablename where a>10 and b <20 limit 10")
        assert ("a,b,c", "tablename", "a>10 and b <20", 10) == qc.parse()

    def test_query_parser_multiline(self):
        # Multiline
        qc = QueryParser(
            """
        SELECT *
        FROM monki
        """
        )
        assert ("*", "monki", None, None) == qc.parse()

        qc = QueryParser(
            """
        SELECT name
        FROM tablename
        where name='bheem'
        limit 10
        """
        )
        assert ("name", "tablename", "name='bheem'", 10) == qc.parse()


class TestQueryParserInsert:
    def test_query_parser_insert_simple(self):
        # Simple
        qc = QueryParser("INSERT INTO person(id,age,name) VALUES(3,32,'Phoebe')")
        assert ("person", "id,age,name", "3,32,'phoebe'") == qc.parse()

    def test_query_parser_insert_multiline(self):
        # Multiline
        qc = QueryParser(
            """
        INSERT INTO
        person (id,age,name)
        values (3,32,'Phoebe')
        """
        )
        assert ("person", "id,age,name", "3,32,'phoebe'") == qc.parse()


class TestQueryParserCreate:
    def test_create_database(self):
        qc = QueryParser("CREATE database bruh")
        assert ("database", "bruh") == qc.parse()

    def test_create_table(self):
        qc = QueryParser("CREATE table hello")
        assert ("table", "hello") == qc.parse()
