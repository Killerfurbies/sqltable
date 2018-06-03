import yaml

def parse_yaml(filename):
    with open(filename, 'r') as yml:
        res = yaml.load(yml)
    return res

databases = parse_yaml('sqltable/conf/databases.yaml')