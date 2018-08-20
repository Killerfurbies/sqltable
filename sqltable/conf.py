import os
import yaml
_conf_path = os.path.join(os.path.expanduser('~'), '.sqltable.conf')

def _parse_yaml(filename):
    with open(filename, 'r') as yml:
        res = yaml.load(yml)
    return res

def reload(conf_file=_conf_path):
    return _parse_yaml(conf_file)

conf = _parse_yaml(_conf_path)
