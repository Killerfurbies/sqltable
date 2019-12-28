import os
from os.path import abspath, dirname, join, expanduser
import subprocess

import psycopg2
import yaml

from sqltable.tools.exceptions import ConfigError, ArgError

SQL_DIR = abspath(join(dirname(dirname(__file__)), 'sql'))


def pgenv(**kwargs):
    """
    Look up a pgpass entry for one or more of the input kwargs. Defaults
    to PG environment variables.
    """
    pg_var_map = {
        'dbname': "PGDATABASE",
        'host': "PGHOST",
        'port': "PGPORT",
        'user': "PGUSER",
        'password': 'PGPASSWORD'
    }
    creds = {}
    unexpected_kwargs = kwargs.keys() - set(pg_var_map.keys())
    if unexpected_kwargs:
        raise ArgError(fun_name='pgenv', passed_value=unexpected_kwargs, expected_value=pg_var_map.keys())

    for k, v in pg_var_map.items():
        item = kwargs.get(k) or os.getenv(v)
        if not item and k != 'password':
            raise EnvironmentError(f"{v} environment variable not set, with no default passed.")
        if item:
            creds[k] = item
    return creds


def pgpass(*args):
    """
    Search ~/.pgpass for an entry.
    """
    if not args:
        raise ArgError(fun_name='pgpass', msg='No arguments supplied')
    cmd = f"cat ~/.pgpass | grep {' | grep '.join(args)}"
    entries = [x for x in subprocess.check_output(cmd, shell=True).decode().split('\n') if x]
    if len(entries) != 1:
        msg = f"{len(entries)} matches were found for args {args}, when one match was expected."
        raise ConfigError(msg)

    entry = entries[0].split(":")
    return {
        'host': entry[0],
        'port': entry[1],
        'dbname': entry[2],
        'user': entry[3],
        'password': entry[4]
    }


def yaml_pass(profile, path=expanduser("~/dbobject.conf"), **kwargs):
    with open(path, 'r') as f:
        conf = yaml.full_load(f)
    try:
        creds = conf['connections'][profile]
    except KeyError:
        raise ConfigError(f"Connection profile '{profile}' not defined in {path}")
    # allow alternate spelling dbname
    if 'database' in creds:
        creds['dbname'] = creds['database']
        del creds['database']
    creds.update(kwargs)
    return pgenv(**creds)


def connect(*args, **kwargs):
    creds = {}
    try:
        creds = yaml_pass(*args, **kwargs)
    except (TypeError, ConfigError):
        pass

    try:
        creds = pgpass(*args)
    except (ArgError, ConfigError):
        pass

    try:
        creds = pgenv(**kwargs)
    except EnvironmentError:
        pass

    if not creds:
        raise ArgError(fun_name='connect', msg="Could not find credentials")

    return psycopg2.connect(**creds)