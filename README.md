# StupidDB

I was really overwhelmed with the amount of functionality contained in standard ORMs such as Mybatis/Ibatis.  Additionally, I actually like working with SQL so I find little advantage in abstracting this logic into model classes as seen by those nifty MVC frameworks.  Honestly, this is probably not an ORM at all as much as it is a method for organizing SQL and removing it from code.

### Configration

The app assumes that you have a config file with the following parameters in the application root:
* db_user=<username>
* db_password=<password>
* db_host=<hostname>
* db_port=<port>
* db_connectdb=<connect_db>
* db_type=<postgresql/mysql>

This class was originally written to work with Redshift (Postgresql) but has been extended to MySQL

### How to use this StupidDB

It's realy quick and easy with 3 methods to remember.  First, instanciate a class:

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

* sqlmap refers to the xml file containing the relevant set of queries (see sqlmap/example.xml)
* id refers to the name of the query being called (see sqlmap/example.xml)
* **kwargs all named parameters that will be used in the query (match in sqlmap is required)

read_single
===========

Same as read_single accepts returns a single dict

```python
stupid->read_single(<sqlmap>, <id>, <**kwargs>)
```

write
=====

This ecompasses all inserts, updates, merges (DML statements, see sqlmap/example.xml)

```python
self->write(<sqlmap>, <id>, <**kwargs>)
```

