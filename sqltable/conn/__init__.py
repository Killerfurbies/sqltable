import importlib
from sqltable.conf import conf


class Conn(object):
    _arg_map = {
        'postgres': {
            'method': ['psycopg2', 'connect'],
            'kwargs': {
                'database': ['dbname'],
                'username': ['user'],
                'password': ['password'],
                'host': ['host'],
                'port': ['port']
            }
        }
    }

    def __init__(self, conn_name):
        self.conn_params = conf['connections'][conn_name]
        self._arg_map = self._arg_map[self.conn_params['type']]
        self.__conn = self._connect()

    def _arg_switch(self):
        # from param_map['method'][0] import param_map['method'][1]
        out_dict = {}
        for k, v in self.conn_params.items():
            if self._arg_map['kwargs'].get(k) is not None:
                out_dict[self._arg_map['kwargs'].get(k)[0]] = v
        return out_dict

    def _connect(self):
        method = self._arg_map['method']
        package = importlib.import_module(method[0])
        connect = getattr(package, method[1])
        kwargs = self._arg_switch()
        conn = connect(**kwargs)
        return conn

    def explain(self, query):
        with self.__conn.cursor() as cur:
            cur.execute('explain ' + query)
            query_plan = cur.fetchall()
        return query_plan

