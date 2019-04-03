from sqltable.conf import conf, reload

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

conn_params = conf['connections']['postgres-local']
param_map = _arg_map[conn_params['type']]


def arg_switch(_arg_map, conn_params):
    param_map = _arg_map[conn_params['type']]
    # from param_map['method'][0] import param_map['method'][1]
    out_dict = {}
    for k, v in conn_params.items():
        if param_map['kwargs'].get(k) is not None:
            out_dict[param_map['kwargs'].get(k)[0]] = v
    return out_dict

test = arg_switch(_arg_map, conn_params)
from psycopg2 import connect