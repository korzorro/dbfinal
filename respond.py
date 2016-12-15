from collections import OrderedDict
from helper import generate_ui, is_integer
from getpass import getpass
from datetime import datetime


database = 'suggestion_box.db'
input_prompt = 'Select a function (enter a number or enter "q" to exit).\n'
again_prompt = 'Would you like to select another function (Enter "y" to ' +\
               'start again)?\n'


# Simple fake login function for user. Checks username and password against
# database and either fails and reprompts or succeeds and returns the user
# information.
def login(conn):
    user = None
    while user is None:
        username = input('Username: ')
        password = getpass('Password: ')
        cursor = conn.execute(
            '''
            SELECT * FROM user WHERE username=\'%s\' AND password=\'%s\'
            AND is_active=1
            '''
            % (username, password)
        )
        user = cursor.fetchone()
        if user:
            print('You have successfully logged in.')
            return user
        print('The login attempt has failed.')


# This prompts users to select a suggestion to respond to. A suggestion_id is
# returned so that it may be used to be link a response with a suggestion.
def get_suggestion_id(conn):
    cursor = conn.execute(
        '''
        SELECT text, id FROM suggestion
        '''
    )
    cursor = list(enumerate(cursor))
    for num, record in cursor:
        print('%i. %s' % (num+1, record[0]))
    user_input = input('Which suggestion would you like to respond to ' +
                       '(select a number)?\n')
    while not (is_integer(user_input) and int(user_input) in
               range(1, len(cursor))):
        user_input = input('Invalid selection: Enter a number from 1 to %i' %
                           len(cursor)+1)

    return cursor[int(user_input)-1][1][1]


# Checks to see if a user has a permission. The permission is searched by name
# if at least one record is recovered from the select statement, this user has
# the specified permission.
def has_permission(user, permission, conn):
    user_id = user[0]
    cursor = conn.execute(
        '''
        SELECT * FROM user
        JOIN user_role ON user_id=user.id
        JOIN role_permission ON user_role.role_id=role_permission.role_id
        JOIN permission ON permission_id=permission.id
        WHERE user.id=%s AND permission.name=\'%s\'
        ''' % (user_id, permission)
    )
    return cursor.fetchone()


# Goes through the necessary prompts for logging in, checking permission and
# entering a response to a selected suggestion. If the user does not have
# permission, the program exits.
def respond(conn):
    user = login(conn)
    if has_permission(user, 'Respond', conn):
        suggestion_id = get_suggestion_id(conn)
        response = input('Enter your response:\n')
        cursor = conn.execute(
            '''
            INSERT INTO response (id, user_id, suggestion_id, text, timestamp)
            VALUES (NULL, %s, %s, \'%s\', \'%s\')
            '''
            % (user[0], suggestion_id, response,
               datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        )
        conn.commit()
        print('The response has been posted.')
        return cursor
    print('This user does not have permission to respond to suggestions.')
    print('Exiting...')
    exit()


functions = OrderedDict([
    ('Respond to Suggestion', respond)
])


if __name__ == '__main__':
    generate_ui(database, functions, input_prompt, again_prompt)
