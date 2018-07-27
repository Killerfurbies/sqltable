import os
import yaml

def _parse_yaml(filename):
    with open(filename, 'r') as yml:
        res = yaml.load(yml)
    return res

_conf_path = os.path.join(os.path.expanduser('~'), '.sqltable.conf')
conf = _parse_yaml(_conf_path)
