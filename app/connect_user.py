import bcrypt
import re

from setup_logging import setup_logger
from queries import (
    sql_query_insert_record_person, sql_query_check_password_person,
    sql_query_check_username_person)
from connect_db import connect

class User:
    """
    """

    def __init__(self, 
        username, 
        password, 
        register_flag,
        login_flag):
        """
        Constructor of class Register.
        """
        self.username = username
        self.password = password
        self.register_flag = register_flag
        self.login_flag = login_flag
        self.logger = setup_logger('ConnectUser')

        self.success_register = False
        self.success_login = False

        self.sql_query_insert_record_person = sql_query_insert_record_person
        self.sql_query_check_password_person = sql_query_check_password_person
        self.sql_query_check_username_person = sql_query_check_username_person

    def connect_user_to_app(self):
        """
        """
        console_msg_register = ''
        console_msg_login = ''

        cursor, connection = connect()

        if self.register_flag:
            console_msg_register = self.register(self.username, self.password,
                cursor, connection)

        if self.login_flag:
            console_msg_login = self.login(self.username, self.password, cursor)

        return self.success_register, self.success_login, console_msg_register, console_msg_login

    def register(self, username, password, cursor, connection):
        """
        """
        console_msg_register = ''

        cursor.execute(self.sql_query_check_username_person, [username])

        if cursor.fetchone()[0]:
            self.success_register = False
            console_msg_register = 'Someone else is using that username. Choose another one.'
        else:
            if re.fullmatch(r'^(?=.*[!@#$%^&*-+_])(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,250}$', password):
                try:
                    password = password.encode('utf-8')
                    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

                    cursor.execute(self.sql_query_insert_record_person, 
                        (username, hashed_password.decode('utf-8')))
                    connection.commit()

                    self.success_register = True
                except Exception as e:
                    self.logger.error(f"{type(e).__name__}: {e}")
            else:
                self.success_register = False
                console_msg_register = 'Invalid password. Try again.'
        
        return console_msg_register
    
    def login(self, username, password, cursor):
        """
        """
        console_msg_login = ''

        try:
            cursor.execute(self.sql_query_check_password_person, [username])
            fetch_select_value = cursor.fetchone()

            if fetch_select_value == None:
                console_msg_login = 'You are not registered.'
                self.success_login = False
            else:
                retrieve_password = fetch_select_value[0]
                retrieve_password = retrieve_password.encode('utf-8')

                password = password.encode('utf-8')

                if bcrypt.checkpw(password, retrieve_password):
                    self.success_login = True
                else:
                    self.success_login = False
                    console_msg_login = 'Invalid credentials. Please try again.'
        except Exception as e:
            self.logger.error(f"{type(e).__name__}: {e}")
        
        return console_msg_login
