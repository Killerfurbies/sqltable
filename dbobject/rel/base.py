import abc
from os.path import dirname, join

import psycopg2

from dbobject.tools.exceptions import ArgError

SQL_DIR = join(dirname(__file__), 'sql')


class Relation:

    __metaclass__ = abc.ABCMeta
    _conn = None
    _metadata = None

    def __init__(self, rel_name, conn):
        self.conn = conn
        self.rel_name = rel_name
        self.schema, self.name = rel_name.split(".")

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, val):
        if not isinstance(val, psycopg2.extensions.connection):
            raise ArgError('conn', expected_dtype=psycopg2.extensions.connection)
        self._conn = val

    def metadata(self):
        if self._metadata is None:
            with open(join(SQL_DIR, 'get_{}_metadata.sql'), 'r') as f:
                query = f.read()
