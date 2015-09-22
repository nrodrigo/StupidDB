from config import Config
from xml.dom import minidom
import os
import os.path
import re
import sys

class StupidDB:
    def __init__(self):
        cfg = Config()
        if cfg.db_type == 'postgres':
            import psycopg2
            import psycopg2.extras
            try:
                self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s' port='%s'" %
                    (cfg.db_connectdb, cfg.db_user, cfg.db_host, cfg.db_password, cfg.db_port))
                self.conn.autocommit = True
            except psycopg2.OperationalError as e:
                sys.exit("Unable to connect to Postgred DB: %s" % __file__)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        elif cfg.db_type == 'mysql':
            import MySQLdb
            import MySQLdb.cursors
            try:
                self.conn = MySQLdb.connect(
                    user=cfg.db_user,
                    host=cfg.db_host,
                    passwd=cfg.db_password,
                    db=cfg.db_connectdb,
                    port=int(cfg.db_port),
                    cursorclass=MySQLdb.cursors.DictCursor
                    )
                self.conn.autocommit(True)
                #self.cur = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                self.cur = self.conn.cursor()
            except MySQLdb as e:
                sys.exit("Unable to connect to MySQL DB: %s" % __file__)
        else:
            sys.exit("cfg.db_type %s undefined.  Please set as either postgres or mysql: %s" % (cfg.db_type, __file__))

        if hasattr(cfg, 'sqlmap_path'):
            self.sqlmap_dir = cfg.sqlmap_path
        else:
            self.sqlmap_dir = cfg.app_root+"/sqlmap"

        if not os.path.isdir(self.sqlmap_dir):
            sys.exit("SQL map path doesn't exist: %s %s" % (self.sqlmap_dir, __file__))

    def __get_sql(self, sql_map, id, type, **kwargs):
        sql_map_path = self.sqlmap_dir+"/"+sql_map+".xml"
        if os.path.isfile(sql_map_path):
            xmldoc = minidom.parse(sql_map_path)
            item_list = xmldoc.getElementsByTagName(type)
            sql = ""
            for item in item_list:
                if item.getAttribute("id") == id:
                    # strip blank lines or any lines consisting of only spaces
                    sql = os.linesep.join([s for s in item.firstChild.nodeValue.splitlines() if s and not s.isspace()])
                    # for any submitted parameters, let's make sure they exist in the query
                    if item.getAttribute("parameters"):
                        sql_parameters = item.getAttribute("parameters").split(",")
                        call_parameters = kwargs.keys()
                        if set(sql_parameters).issubset(set(call_parameters)) and set(sql_parameters).issuperset(set(call_parameters)):
                            for key, value in kwargs.iteritems():
                                sql = sql.replace("{"+key+"}", str(value))
                        else:
                            sys.exit("SQL map parameters (%s) don't match calling parameters (%s); id=%s %s" %
                                (",".join(sql_parameters), ",".join(call_parameters), id, __file__))
            if not sql:
                sys.exit("Unable to find query: type=%s, id=%s %s" % (type, id, __file__))
        else:
            sys.exit("SQL map doesn't exist: %s %s" % (sql_map, __file__))
        return sql

    def exec_sql(self, sql_map, id, type, **kwargs):
        sql = self.__get_sql(sql_map, id, type, **kwargs)
        try:
            self.cur.execute(sql)
        except psycopg2.Error, e:
            sys.exit("Unable to execute query: type=%s, id=%s\n %s %s" % (type, id, e.pgerror, __file__))

    def read(self, sql_map, id, **kwargs):
        self.exec_sql(sql_map, id, "read", **kwargs)
        res = self.cur.fetchall()
        return res

    def read_single(self, sql_map, id, **kwargs):
        self.exec_sql(sql_map, id, "read_single", **kwargs)
        if self.cur.rowcount>1:
            sys.exit("Query returns more than 1 row.  Use self->select. %s %s" % (id, __file__))
        else:
            return self.cur.fetchone()

    def write(self, sql_map, id, **kwargs):
        self.exec_sql(sql_map, id, "write", **kwargs)

