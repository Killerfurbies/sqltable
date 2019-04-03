import os
import subprocess


def pgpass(dbname=None, host=None, port=None, user=None):
    """
    Look up a pgpass entry for one or more of the input kwargs. Defaults
    to PG environment variables.
    """
    dbname = dbname or os.getenv("PGDATABASE")
    host = host or os.getenv("PGHOST")
    port = port or os.getenv("PGPORT")
    user = user or os.getenv("PGUSER")
    lookups = []
    for var in [dbname, host, port, user]:
        if var:
            lookups.append("grep %s" % var)
    cmd = "cat ~/.pgpass | {}".format(" | ".join(lookups))
    return subprocess.check_output(cmd, shell=True)



