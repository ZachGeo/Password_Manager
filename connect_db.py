import psycopg2

from configparser import ConfigParser

def connect(ini_filename='db.ini'):
    parser = ConfigParser()
    parser.read(ini_filename)
    connection_info = {param[0]: param[1] for param in parser.items("postgres")}

    connection = psycopg2.connect((
        f"dbname=password_manager " \
        f"user={connection_info['user']} " \
        f"password={connection_info['password']} " \
        f"port={connection_info['port']}"))      

    cursor = connection.cursor()

    return cursor, connection
