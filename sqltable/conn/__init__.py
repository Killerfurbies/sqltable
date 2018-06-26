import yaml
import os
import importlib

#class DbConn(object):
arg_map = {
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

method = arg_map['postgres']['method']
package = importlib.import_module(method[0])
connect = getattr(package, method[1]

with open(
#make_dict(in_dict):
	
