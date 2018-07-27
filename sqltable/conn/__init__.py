import yaml
import os
import importlib
from sqltable.conf import conf

class Conn(object):
	_arg_map = {
	'postgres': {
		'method': ['psycopg2', 'connect'],
		'kwargs': { 
			'database': ['dbname'],
			'user': ['user'],
			'password': ['password'],
			'host': ['host'],
			'port': ['post']
			}	
		}
	}


def _arg_switch(conn_name, arg_map):
	

method = arg_map['postgres']['method']
package = importlib.import_module(method[0])
connect = getattr(package, method[1]

with open(
#make_dict(in_dict):
	
