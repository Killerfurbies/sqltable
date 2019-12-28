import re

class Query(object):
    """
    Wrapper for SQL select statements
    Version 1: Read .sql or sql string file and verify against connection
    Version 2: Build query
    Version 3: ETL functions such as to_file(), to_df(), to_sqltable()
    """

    def __init__(self, conn, sql):
        self._raw_sql = sql
        self.query = self.load_sql()
        self.conn = conn
        # This step validates the query against the database
        self.plan = self.conn.plan(self.query)

    def load_sql(self):
        # if string ends in .sql, load from file
        # if string begins with select, load from string

    def _load_from_file(self):
        pass

    def _load_from_string(self):
        pass

