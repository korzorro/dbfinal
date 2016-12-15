from collections import OrderedDict
from helper import generate_ui
from getpass import getpass
from copy import deepcopy


database = 'suggestion_box.db'
input_prompt = 'Select a function (enter a number or enter "q" to exit).\n'
again_prompt = 'Would you like to select another function (Enter "y" to ' +\
               'start again)?\n'


def login(conn):
    username = input('Username: ')
    password = getpass('Password: ')
    cursor = conn.execute(
        '''
        SELECT * FROM user WHERE username=\'%s\' AND password=\'%s\'
        AND is_active=1
        '''
        % (username, password)
    )
    if len(cursor.fetchall()):
        print('You have successfully logged in as...')
    else:
        print('The login attempt has failed.')

    cursor = conn.execute(
        '''
        SELECT username, email
        FROM user WHERE username=\'%s\' AND password=\'%s\'
        AND is_active=1
        '''
        % (username, password)
    )

    return cursor

functions = OrderedDict([
    ('Login', login)
])
if __name__ == '__main__':
    generate_ui(database, functions, input_prompt, again_prompt)
