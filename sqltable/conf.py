import os
import yaml

def parse_yaml(filename):
    with open(filename, 'r') as yml:
        res = yaml.load(yml)
    return res

conf = os.path.join('/Users/', os.environ.get('USER'), '.sqltable.conf')
databases = parse_yaml(conf)
