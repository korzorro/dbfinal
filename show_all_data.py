from collections import OrderedDict
from helper import generate_ui

database = 'suggestion_box.db'
input_prompt = 'What table would you like to view all of the records of ' +\
               '(enter a number or enter\n"q" to exit)?\n'
again_prompt = 'Would you like to view the records of another table (Enter' +\
               '"y" to start again)?\n'


def show_suggestions(conn):
    return conn.execute(
        '''
        SELECT text, author, email, phone, timestamp, is_public, should_contact
        FROM suggestion
        '''
    )


def show_responses(conn):
    return conn.execute(
        '''
        SELECT suggestion.text as suggestion_text, response.text as
        response_text, username, full_name, response.timestamp
        FROM response
        JOIN user ON user_id=user.id
        JOIN suggestion ON suggestion_id=suggestion.id
        '''
    )


def show_comments(conn):
    return conn.execute(
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


def show_users(conn):
    return conn.execute(
        '''
        SELECT username, full_name, email, password, is_active,
        GROUP_CONCAT(role.name, \', \') as roles
        FROM user
        JOIN user_role ON user.id=user_id
        JOIN role ON role.id=role_id
        GROUP BY user.id
        '''
    )


# This function and show_permissions both make use of views in order to
# simplify the slect statement. This may not be efficient but it aided in the
# logic.
def show_roles(conn):
    return conn.execute(
        '''
        SELECT role_users_concat.name, users, permissions FROM
        role_users_concat JOIN role_permissions_concat ON
        role_users_concat.id=role_permissions_concat.id
        '''
    )


def show_permissions(conn):
    return conn.execute(
        '''
        SELECT permission.name, endpoint, GROUP_CONCAT(role.name, \', \')
        as roles
        FROM permission
        JOIN role_permission ON permission_id=permission.id
        JOIN role ON role.id=role_id
        GROUP BY permission.id
        '''
        )


functions = OrderedDict([
    ('suggestion', show_suggestions),
    ('response', show_responses),
    ('comment', show_comments),
    ('user', show_users),
    ('role', show_roles),
    ('permission', show_permissions)
])


if __name__ == '__main__':
    generate_ui(database, functions, input_prompt, again_prompt)
