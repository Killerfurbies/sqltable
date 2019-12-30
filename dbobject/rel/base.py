import abc
from os.path import dirname, join

import psycopg2

from dbobject.tools.exceptions import ArgError

SQL_DIR = join(dirname(__file__), 'sql')


class Relation:

    _metadata = None
    owner = None
    

    def __init__(self, rel_name, conn):
        if not isinstance(conn, psycopg2.extensions.connection):
            raise ArgError('conn', expected_dtype=psycopg2.extensions.connection)
        self.conn = conn
        self.rel_name = rel_name
        self.schema, self.name = rel_name.split(".")
        self._validate_rel_kind()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'rel_kind'):
            raise NotImplementedError("Class attribute 'rel_kind' must be defined.")

    def _validate_rel_kind(self):
        with open(join(SQL_DIR, 'get_relation_metadata.sql'), 'r') as f:
            query = f.read().format(schema=self.schema, name=self.name)
        with self.conn.cursor() as csr:
            csr.execute(query)
            

    def metadata(self):
        if self._metadata is None:
            with open(join(SQL_DIR, 'get_{}_metadata.sql'), 'r') as f:
                query = f.read()
