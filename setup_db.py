#!/usr/bin/python3

import psycopg2

from setup_logging import setup_logger
from configparser import ConfigParser
from queries import sql_query_table_person, sql_query_table_login_data

class SetupDB:
    """
    A class to setupt the database.
    ...

    Attributes
    ----------
    logger_name: str
        name of the logger
    ini_filename: str
        postgres database info
    table_names: list
        names of the tables of the database

    Methods
    -------
    setup():
        Setup database and tables of the program.
    load_connection_info(ini_filename):
        Load the parameters for the connection to the database.
    create_db(conn_info):
        Create the database.
    create_tables(conn, cur, *sql_queries):
        Create the tables.
    """

    def __init__(self, 
        logger_name='SetupDB', 
        ini_filename='db.ini', 
        table_names=['person', 'login_data']):
        """
        Constructs all the necessary attributes for the SetupDB object.

        Parameters
        ----------
            logger_name: str
                name of the logger
            ini_filename: str
                postgres database info
            table_names: list
                names of the tables of the database
        """
        self.logger = setup_logger(logger_name)
        self.ini_filename = ini_filename
        self.table_names = table_names
        self.conn_info = {}

        self.sql_query_table_person = sql_query_table_person
        self.sql_query_table_login_data = sql_query_table_login_data
    
    def setup(self):
        """
        Setup the database and the tables. Create all the neccesary logs.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.load_connection_info(self.ini_filename)
        if self.conn_info:
            self.logger.info('Load connection info of Postgres')

            psql_connection_info = f"dbname={self.conn_info['dbname']} " \
                f"user={self.conn_info['user']} " \
                f"password={self.conn_info['password']} " \
                f"port={self.conn_info['port']}" 
                
            check_db = self.create_db(psql_connection_info)

            connection = psycopg2.connect((
                f"dbname=password_manager " \
                f"user={self.conn_info['user']} " \
                f"password={self.conn_info['password']} " \
                f"port={self.conn_info['port']}"))         
            cursor = connection.cursor()

            if check_db:
                self.logger.info('Database has been created')

                check_tables = self.create_tables(connection, 
                    cursor, 
                    self.sql_query_table_person, 
                    self.sql_query_table_login_data)
                
                if check_tables:
                    self.logger.info('Tables have been created')
                else:
                    self.logger.info('Tables do not exist')
            else:
                self.logger.info('Database does not exist')
            
            connection.close()
            cursor.close()
        else:
            self.logger.info('Connection to Postgres could not esablished')

    def load_connection_info(self, ini_filename):
        """
        Load the parameters of the database connection from the ini file.

        Parameters
        ----------
        ini_filename: str, compulsory
            File containing parameters of postgres.

        Returns
        -------
        None
        """
        parser = ConfigParser()
        parser.read(ini_filename)
        conn_info = {param[0]: param[1] for param in parser.items("postgres")}

        self.conn_info = conn_info

    def create_db(self, conn_info):
        """
        Create the database.

        Parameters
        ----------
        conn_info: str, compulsory
            Data for connecting to the postgres database.
        Returns
        -------
        check_creation_db: boolean
            Boolean value if database was created or not.
        """
        conn = psycopg2.connect(conn_info)
        conn.autocommit = True
        cur = conn.cursor()

        sql_query = f"CREATE DATABASE password_manager"

        try:
            cur.execute(sql_query)
        except Exception as e:
            self.logger.error(f"{type(e).__name__}: {e}")
            cur.execute("DROP DATABASE password_manager")
        else:
            conn.autocommit = False 
            cur.execute(
                "SELECT datname FROM pg_catalog.pg_database " \
                "WHERE datname = 'password_manager';"
            )
            check_creation_db = cur.fetchone()[0]

        cur.close()
                    
        return check_creation_db

    def create_tables(self, conn, cur, *sql_queries):
        """
        Create the tables of the database.
            
        Parameters
        ----------
        conn: str, compulsory
            
        cur: str, compulsory

        *sql_queries: tuple, compulsory
            Sql queries for tables creation.

        Returns
        -------
        check_creation_tables: boolean
            Boolean value if tables was created or not.
        """
        check_creation_tables = []

        for query in sql_queries:
            try:
                cur.execute(query)
            except Exception as e:
                self.logger.error(f"{type(e).__name__}: {e}")
                conn.rollback()
                cur.execute(f"DROP TABLE IF EXISTS {self.tables[0]} CASCADE")
            else:
                conn.commit()           
                for name in self.table_names: 
                    cur.execute("SELECT COUNT(*) FROM information_schema.tables " \
                        "WHERE table_schema='public';")
                    check_creation_tables = cur.fetchone()[0]
        
        cur.close()
        
        check_creation_tables = True if check_creation_tables == 2 else False
        
        return check_creation_tables

if __name__ == "__main__":
    db = SetupDB()
    db.setup()
