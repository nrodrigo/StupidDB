# StupidDB

I was looking for a really easy way to organize SQL outside of code.  Standard ORMs just seem to have way more functionality then I actually need and object models just seem to kill all that is great with SQL.  Additionally, I actually like working with SQL and found little use for proper models in my projects.  So thus, all I really needed was a stupid simple python module to communicate with the database and provide an ORM'ish type framework to organize SQL.

StupidDB supports PostgreSQL (psycopg2) and MySQL (MySQLdb).  One caveat is that there is no restriction to writing db-specific SQL in your SQL map files.  StupidDB provides no abstraction as far as the database layer is concerned.  But really, how often are you gonna swap the underlying DB?  Plus, with little restriction on the DB layer, you can take advantage of more advanced DB-specific features (analytical functions and stuff).

### Configuration

Place your _config_ file in the root of your application and specify the following arguments:
* db_user=_username_
* db_password=_password_
* db_host=_hostname_
* db_port=_port_
* db_connectdb=_connect_db_
* db_type=_postgresql/mysql_
* sqlmap_path=_path to sqlmap directory_ _(optional: by default, assumes a sqlmap directory exists in your application root)_


### How to use this StupidDB

It's realy quick and easy with 3 methods to remember.  First, instantiate a class:

```python
from StupidDB.stupiddb import StupidDB
stupid = StupidDB()
```

You might need to modify the import statement depending on how your environment is setup.

read
====

This encompasses any and all queries meant to return as a list of dicts.  As a consumer, the call is as follows:

```python
results = stupid->read(<sqlmap>, <id>, <**kwargs>)
```

* sqlmap refers to the xml file containing the relevant set of queries (see [sqlmap/example.xml](sqlmap/example.xml))
* id refers to the name of the query being called (see [sqlmap/example.xml](sqlmap/example.xml))
* **kwargs all named parameters that will be used in the query (match in sqlmap is required)

read_single
===========

Same as read_single accepts returns a single dict

```python
result = stupid->read_single(<sqlmap>, <id>, <**kwargs>)
```

write
=====

This ecompasses all inserts, updates, merges (DML statements, see [sqlmap/example.xml](sqlmap/example.xml))

```python
stupid->write(<sqlmap>, <id>, <**kwargs>)
```

And that's it!  Have fun...
