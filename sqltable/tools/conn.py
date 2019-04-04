import os
import subprocess


def pgenv(dbname=None, host=None, port=None, user=None):
    """
    Look up a pgpass entry for one or more of the input kwargs. Defaults
    to PG environment variables.
    """
    creds = dict(dbname=dbname or os.getenv("PGDATABASE"),
                 host=host or os.getenv("PGHOST"),
                 port=port or os.getenv("PGPORT"),
                 user=user or os.getenv("PGUSER")
                 )
    if not all(creds.values()):
        raise ValueError("One or more values is None: \n %r" % creds)
    return creds


def pgpass(dbname=None, host=None, port=None, user=None):
    """
    Look up a pgpass entry for one or more of the input kwargs.
    """
    creds = dict(dbname=dbname, host=host, port=port, user=user)
    lookups = []
    for val in creds.values():
        if val:
            lookups.append("grep %s" % val)
    cmd = "cat ~/.pgpass | {}".format(" | ".join(lookups))
    stdout = subprocess.check_output(cmd, shell=True).decode()
    entries = [x for x in stdout.split() if x]
    if len(entries) > 1:
        raise EnvironmentError("Multiple entries found in .pgpass for: {}".format(", ".join(lookups)))
    if len(entries) == 0:
        raise EnvironmentError("No entries found in .pgpass for: {}".format(", ".join(lookups)))
    entry = entries[0].split(":")
    creds['host'] = entry[0]
    creds['port'] = entry[1]
    creds['dbname'] = entry[2]
    creds['user'] = entry[3]
    return creds
