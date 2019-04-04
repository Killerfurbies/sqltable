import abc

import psycopg2


class Relation:

    __metaclass__ = abc.ABCMeta
    _conn = None

    def __init__(self, conn, relname):
        self.conn = conn

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, val):
        if val.__class__ is not psycopg2.extensions.connection:
            raise NotImplementedError("Relation only implemented for psycopg2 connections")
        self._conn = val

    @abc.abstractmethod
    def metadata(self):
        # grab metadata, checking that the relation exists in the process
        pass