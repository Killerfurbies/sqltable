# sqltable
Tool for querying and ETL

## Outline

Three main classes - Query, DDL, and Connection
1. Connection
	- Supports Query and DDL
	- represents a connection to a database. can be referenced in sqltable-specific config or built from DBI connection object (psycopg2, pypostgres etc)
	- all query objects to be 'evaluated' against the connection to see if they can 'compile' (i.e. run `explain` and catch errors)
2. Query
	- strictly read-only. cannot destroy or edit existing data
	- just a query builder. creates a sql string to be evaluated by RDMBS
	- allows 'global where', which can be set in config or per session. queries cannot disobey global qhere


## Examples


```python
from sqltable import Conn, Query, DDL

conn = Conn(conn=pypostgres.connect(host='127.0.0.1', database='my_db', user='test', password='password', port=3306))
conn = Conn(x='postgres') # where x is a connection profile defined in .sqltable.conf (rename x later)
conn = Conn(uri='postgres://test:password@127.0.0.1/my_db')

query = Query(string='select * from customers', conn=conn)
query = Query(file='sql/customers.sql', conn=conn)
query = Query(relation='customers') # where customers is a table or view in my_db; defaults to select * if table or view def if view

ddl = DDL(string='create customers(id int, name text)', conn=conn)
ddl = DDL(file='sql/create_table_customers.sql', conn=conn)
ddl = DDL(relation='customers', conn=conn)
```

## Query

### Purpose

The most powerful aspect of the `Query` class will be the `global where`. It is a restriction set upon the current session, or within a config file (perhaps set by an administrator) that cannot be disobeyed.

The impetus for this feature was from a company I worked at that shared storage and compute with multiple clients in a multi-tenant environment. Clients were denoted by a unique `id` that was present in a field in most tables. Picking the wrong `id`, or failing to pick any `id`, would have resulted in sending the wrong data to the wrong client, which would have been catastrophic.

Also, it saves time to set a value once rather than having to reference it in every query. Say your data is maintained by an ORM in which records are stamped with a `created_at` value. You want to create weekly reports. You can reference `where created_at between last_week and this_week` in every query, or once at the beginning of the session do:

```python
sqltable.conf.set_global_where("created_at >= '%(last_sunday)s' and created_at < '%(this_sunday)s'" % ...)
```

And this condition is appended to every query where `created_at` is a field in the referenced relations. Very convenient.

It should also give peace of mind to systems administrators, DBAs, Data Engineers and the like who need to give database access to data analysts. They
can supply a connection string to an analyst in an encrypted `.sqltable.conf` file (or better yet, in some encrypted key-value store), ensuring that the analysts can only access the database through this controlled avenue. Since the administrators can supply default global where conditions in `.sqltable.conf`, they can effectively quarantine an analyst to their sphere of responsibility without the hassle of row-level permissions (in databases that support it), or creating complicated user and group permissions. Simply share a config file with whomever you wish.

Or more likely it's used by a superuser who just wants to be diligent. Keep a different `.sqltable.conf` for every report to reduce risk of human error.

### Methods

The `Query` class will access standard SQL clauses as functions.

```python
cust = Query(table='customers', conn=conn)
cust.where("date_of_birth >= '2000-01-01'").\
	group_by("gender").\
	select("count(*)").
cust.query 
# select count(*) from customers whree date_of_birth >= '2000-01-01' group by gender; 

purch = Query(table='purchases', conn=conn)
purch.join(cust, type='left', on='customer_id').\
	where('purchase_date >= date_sub(now() interval 7 days)').\
	group_by('date(purchase_date)').\
	select('count(distinct(purch.customer_id))')
```

## DDL

### Purpose

### Methods

## Conn

### Purpose

### Methods

## Conf

Configuration settings for the current python session. Always looks for local before global.

### Purpose

Security. Convenience. Time.

### Methods
