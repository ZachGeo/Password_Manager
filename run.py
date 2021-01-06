#!/usr/bin/python3

import sys
import time
import csv

from app.connect_user import User
from app.pwmanager import pwManager
from getpass import getpass

def give_credentials():
    username = input('Username: ')
    password = getpass('Password: ')

    return username, password

def password_manager(register_flag=False, login_flag=False):
    print('--------------------------------------')
    print('*         Password Manager App       *')
    print('--------------------------------------')

    while True:
        try:
            user_register_login_option = input('Please type Register or Login: ')
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
        else:
            if user_register_login_option.lower() == 'register':
                register_flag = True
                break
            elif user_register_login_option.lower() == 'login':
                login_flag = True
                break
            else:
                register_flag = False
                login_flag = False
                print("Sorry, invalid input! Please try again.")
                continue

    return register_flag, login_flag

def register(register_flag, login_flag):
    while True:
        print('______________________________________')
        print('              REGISTER                ')

        username, password =  give_credentials()

        user = User(username, password, register_flag, login_flag)
        success_register, success_login, console_msg_register, console_msg_login = user.connect_user_to_app()

        if success_register:
            print('You are successfully registered.')
            login_flag = True
            register_flag = False
            break
        else:
            print(console_msg_register)
            print('\n')
            continue
    return register_flag, login_flag

def login(register_flag, login_flag):
    while True:
        print('______________________________________')
        print('                LOGIN                 ')
        
        username, password =  give_credentials()

        user = User(username, password, register_flag, login_flag)
        success_register, success_login, console_msg_register, console_msg_login = user.connect_user_to_app()

        if success_login:
            print('You are successfully logged in.')
            break
        else:
            print(console_msg_login)
            print('\n')
            continue
    return success_login, user

def select_action():
    user_action = input(': ')

    return user_action

def manager_action(user, action_flag):

    manager = pwManager(user.username, user.password, action_flag)
    result_action = manager.control_actions()

    return result_action

if __name__ == "__main__":
    register_flag, login_flag = password_manager()

    if register_flag:
        register_flag, login_flag = register(register_flag, login_flag)
    
    if login_flag:
        success_login, user = login(register_flag, login_flag)
    while True:
        if success_login:
            print('--------------------------------------')
            print('*                MENU                *')
            print('--------------------------------------')

            print('1. Create new password for an app')
            print('2. Find all passwords and apps connected to an email')
            print('3. Find a password for a site or app')
            print('4. Download all uploaded data')
            print('D. Delete all uploaded data')
            print('Q. Exit')
            print('\n')

            action_flag = select_action()
            result_action, console_msg_manager = manager_action(user, action_flag)
            
            if console_msg_manager:
                print(console_msg_manager)
            else:
                print('______________________________________')
                print('RESULTS:')
                print('\n')
                
                if action_flag == '1':
                    for key, value in result_action.items():
                        print(f'{key}: {value}')

                elif action_flag == '2':
                    for item in result_action:
                        result = {'Username': item[0],
                            'Password': item[1],
                            'App Name': item[2]}
                    
                        for key, value in result.items():
                            print(f'{key}: {value}')
                        print('\n')

                elif action_flag == '3':
                    for item in result_action:
                        result = {'Username': item[0],
                            'Password': item[1],
                            'email': item[2],
                            'url': item[3],
                            'app_name': item[4]}
                    
                        for key, value in result.items():
                            print(f'{key}: {value}')
                        print('\n')

                elif action_flag == '4':
                    data = []
                    data_headers = ['Username', 'Password', 'Email', 'URL', 'App Name']
                    filepath = '/home/zach/password_manager/download_data/export.csv'
                    for item in result_action:
                        result = {'Username': item[0],
                        'Password': item[1],
                        'Email': item[2],
                        'URL': item[3],
                        'App Name': item[4]}
                        data.append(result)

                    
                    try:
                        with open(filepath, 'w') as file:
                            writer = csv.DictWriter(file, fieldnames=data_headers)
                            writer.writeheader()
                            for data in data:
                                writer.writerow(data)
                    except Exception as e:
                        print(f'{e}')
                    else:
                        print('Data have been saved.')
                        print('\n')

                elif action_flag == 'D':
                    print(result_action)

                elif action_flag == 'Q':
                    print(result_action)
                    print('______________________________________')
                    
                    for i in range(1,5):
                        print('SHUTDOWN APP: ' + str(25 *i) + '%')
                        time.sleep(1)
                    
                    sys.exit()
            
            input('Press any key to continue...')
