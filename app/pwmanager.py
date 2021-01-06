from setup_logging import setup_logger
from connect_db import connect
from queries import (sql_query_create_password, sql_query_select_added_data,
    sql_query_select_data_based_on_email, sql_query_select_data_based_on_app,
    sql_query_delete_data_based_on_user, sql_query_all_data_user)
from .connect_user import User


class pwManager(User):
    """
    """
    def __init__(self,  
        username,
        password,      
        action_flag,
        register_flag=False,
        login_flag=False):
        """
        """
        super().__init__(username, password, register_flag, login_flag)

        self.username = username
        self.password = password
        self.action_flag = action_flag
        self.logger = setup_logger('pwManager')

        self.sql_query_create_password = sql_query_create_password
        self.sql_query_select_added_data = sql_query_select_added_data
        self.sql_query_select_data_based_on_email = sql_query_select_data_based_on_email
        self.sql_query_select_data_based_on_app = sql_query_select_data_based_on_app
        self.sql_query_delete_data_based_on_user = sql_query_delete_data_based_on_user
        self.sql_query_all_data_user = sql_query_all_data_user

    def control_actions(self):
        """
        """
        cursor, connection = connect()

        if self.action_flag == '1':
            result, console_msg_manager = self.create_password(cursor, connection)
        elif self.action_flag == '2':
            result, console_msg_manager = self.find_app_connected_to_email(cursor)
        elif self.action_flag == '3':
            result, console_msg_manager = self.find_password_for_app(cursor)
        elif self.action_flag == '4':
            result, console_msg_manager = self.download_data(cursor)
        elif self.action_flag == 'D':
            result, console_msg_manager = self.delete_data(cursor, connection)
        elif self.action_flag == 'Q':
            result, console_msg_manager = self.exit_app(connection)
        else:
            result = False
            console_msg_manager = 'Invalid option'
        
        return result, console_msg_manager

    def create_password(self, cursor, connection):
        """
        """
        result = {}
        console_msg_manager = ''

        app_username = input('Username: ')
        app_password = input('Password: ')
        app_email = input('Email: ')
        app_url = input('URL: ')
        app_name = input('App Name: ')

        try:
            cursor.execute(self.sql_query_create_password, 
                (app_username, app_password, app_email, app_url, app_name, 
                self.username)
            )
            connection.commit()
        except Exception as e:
            self.logger.error(f"{type(e).__name__}: {e}")
            console_msg_manager = 'Invalid input'

        try:
            cursor.execute(self.sql_query_select_added_data, 
                (self.username, app_name))
            inserted_data = cursor.fetchone()
        except Exception as e:
            self.logger.error(f"{type(e).__name__}: {e}")
            console_msg_manager = 'Fetcing data error'
        else:
            result = {'Username': inserted_data[0], 
                'Password': inserted_data[1],
                'Email': inserted_data[2],
                'URL': inserted_data[3],
                'App Name': inserted_data[4]}

        return result, console_msg_manager

    def find_app_connected_to_email(self, cursor):
        """
        """
        result = {}
        console_msg_manager = ''

        app_email = input('Email: ')

        try:
            cursor.execute(self.sql_query_select_data_based_on_email, 
                (self.username, app_email))
            retrieved_data = cursor.fetchall()
        except Exception as e:
            self.logger.error(f"{type(e).__name__}: {e}")
            console_msg_manager = 'Retrieve data error'
        else:
            result = retrieved_data

        return result, console_msg_manager
    
    def find_password_for_app(self, cursor):
        """
        """
        console_msg_manager = ''

        app_name = input('App Name: ')

        try:
            cursor.execute(self.sql_query_select_data_based_on_app, 
                (self.username, app_name))
            retrieved_data = cursor.fetchall()
        except Exception as e:
            self.logger.error(f"{type(e).__name__}: {e}")
            console_msg_manager = 'Retrieve data error'
        else:
            result = retrieved_data

        return  result, console_msg_manager

    def download_data(self, cursor):
        """
        """
        console_msg_manager = ''

        try:
            cursor.execute(self.sql_query_all_data_user, [self.username])
            retrieved_data = cursor.fetchall()
        except Exception as e:
            self.logger.error(f"{type(e).__name__}: {e}")
            console_msg_manager = 'Download data error'
        else:
            result = retrieved_data

        return result, console_msg_manager

    def delete_data(self, cursor, connection):
        """
        """
        console_msg_manager = ''

        try:
            cursor.execute(self.sql_query_delete_data_based_on_user, [self.username])
            connection.commit()
        except Exception as e:
            self.logger.error(f"{type(e).__name__: {e}}")
            console_msg_manager = 'Delete data error'
        else:
            result = 'Your password have been deleted successfully'

        return result, console_msg_manager    
    def exit_app(self, connection):
        """
        """
        console_msg_manager = ''

        connection.close()
        result = 'Connection has closed.'

        return result, console_msg_manager
