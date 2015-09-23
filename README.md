# StupidDB

I was really overwhelmed with the amount of functionality contained in standard ORMs and model classes.  Additionally, I actually like working with SQL so I find it a little more challenging having to work object models as seen by those nifty MVC frameworks.  I whipped together this little db module + ORM'ish type interface.  Honestly, this is probably not an ORM at all as much as it is a method for organizing SQL and removing it from code.

StupidDB supports Postgresql (psycopg2) and MySQL (MySQLdb) although the SQL contained in the SQL map files are specific to either DB.  StupidDB provides no abstraction as far as the database layer is concerned.  How often are you gonna swap underlying DBs really?  Plus, with little restriction on the DB layer, you can take advantage of more advanced DB-specific features (analytical functions and stuff).

### Configuration

The app assumes that you have a config file with the following parameters in the application root:
* db_user=_username_
* db_password=_password_
* db_host=_hostname_
* db_port=_port_
* db_connectdb=_connect_db_
* db_type=_postgresql/mysql_
* sqlmap_path=_path to sqlmap directory_ _(optional)_


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

And that's it!  Have fun...
write
=====

This ecompasses all inserts, updates, merges (DML statements, see [sqlmap/example.xml](sqlmap/example.xml))

```python
stupid->write(<sqlmap>, <id>, <**kwargs>)
```

