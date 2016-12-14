import sqlite3


database = 'suggestion_box.db'
input_prompt = 'What table would you like to view all of the records of ' +\
               '(enter a number or enter "q" to exit)?\n'
again_prompt = 'Would you like to view the records of another table (Enter' +\
               '"y" to start again)?'
tables = ('suggestion', 'response', 'comment', 'user', 'role', 'permission')


def show_options():
    for number, table in enumerate(tables):
        print('%i. %s' % (number+1, table))


def print_records(cursor):
    print('-'*80)
    for record in cursor:
        for i, value in enumerate(record):
            print('%s: %s' % (cursor.description[i][0], value))
        print('-'*80)
        

def show_suggestions(conn):
    cursor = conn.execute(
        '''
        SELECT text, author, email, phone, timestamp, is_public, should_contact
        FROM suggestion
        '''
    )
    print_records(cursor)


def show_responses(conn):
    cursor = conn.execute(
        '''
        SELECT suggestion.text as suggestion_text, response.text as
        response_text, username, full_name, response.timestamp
        FROM response
        JOIN user ON user_id=user.id
        JOIN suggestion ON suggestion_id=suggestion.id
        '''
    )
    print_records(cursor)


def show_comments(conn):
    cursor = conn.execute(
        '''
        SELECT suggestion.text as suggestion_text, response.text as
        response_text, comment.text as comment_text, username as commenter,
        full_name, response.timestamp
        FROM comment
        JOIN user ON comment.user_id=user.id
        JOIN response ON response_id=response.id
        JOIN suggestion ON suggestion_id=suggestion.id
        '''
    )
    print_records(cursor)


def show_users(conn):
    cursor = conn.execute(
        '''
        SELECT username, full_name, email, password, is_active,
        GROUP_CONCAT(role.name, \', \') as roles
        FROM user
        JOIN user_role ON user.id=user_id
        JOIN role ON role.id=role_id
        GROUP BY user.id
        '''
    )
    print_records(cursor)


def show_roles(conn):
    cursor = conn.execute(
        '''
        SELECT role_users_concat.name, users, permissions FROM
        role_users_concat JOIN role_permissions_concat ON
        role_users_concat.id=role_permissions_concat.id
        '''
    )
    print_records(cursor)


def show_permissions(conn):
    cursor = conn.execute(
        '''
        SELECT permission.name, endpoint, GROUP_CONCAT(role.name, \', \')
        as roles
        FROM permission
        JOIN role_permission ON permission_id=permission.id
        JOIN role ON role.id=role_id
        GROUP BY permission.id
        '''
        )
    print_records(cursor)


functions = {'suggestion': show_suggestions,
             'response': show_responses,
             'comment': show_comments,
             'user': show_users,
             'role': show_roles,
             'permission': show_permissions}


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_table_name():
    show_options()
    user_input = input(input_prompt)
    while user_input != 'q':
        if is_integer(user_input):
            user_input = int(user_input)
        if user_input in range(1, len(tables)+1):
            return tables[user_input-1]
        print('Invalid selection: Enter a number from 1 to %i' % len(tables))
        user_input = input()

if __name__ == '__main__':
    conn = sqlite3.connect(database)
    again = 'y'
    while again == 'y':
        table_name = get_table_name()
        if table_name is None:
            break
        functions[table_name](conn)
        again = input(again_prompt)
