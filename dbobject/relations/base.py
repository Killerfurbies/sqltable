import abc

import psycopg2

from sqltable.tools.conn import read_sql


class Relation:

    __metaclass__ = abc.ABCMeta
    _conn = None

    def __init__(self, conn, rel_name):
        self.conn = conn
        self.rel_name = rel_name
        self.schema, self.name = rel_name.split(".")

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, val):
        if val.__class__ is not psycopg2.extensions.connection:
            raise NotImplementedError("Relation only implemented for psycopg2 connections")
        self._conn = val

    def metadata(self):
        query = read_sql("slash_d.sql").format(schema=self.schema, name=self.name)
        data =