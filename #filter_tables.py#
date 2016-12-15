from helper import generate_ui
from collections import OrderedDict

database = 'suggestion_box.db'
input_prompt = 'Select a function (enter a number or enter "q" to exit).\n'
again_prompt = 'Would you like to select another function (Enter "y" to ' +\
               'start again)?\n'


def filter_active_users(conn):
    is_active = input('Type 0 to view inactive users or 1 to view active ' +
                      'users.\n')
    while is_active not in ('0', '1'):
        is_active = input('Please enter 0 or 1.\n')

    return conn.execute(
        '''
        SELECT username, full_name, email, password
        FROM user WHERE is_active=%s
        '''
        % is_active
    )


def find_user(conn):
    username = input('Enter a username to lookup.\n')
    return conn.execute(
        '''
        SELECT username, full_name, email, password
        FROM user WHERE username=\'%s\'
        '''
        % username
    )


def filter_unconcacted_suggestors(conn):
    return conn.execute(
        '''
        SELECT author, email, phone, text, timestamp
        FROM suggestion WHERE should_contact=1
        '''
    )


def filter_suggestions_without_responses(conn):
    return conn.execute(
        '''
        SELECT author, email, phone, suggestion.text, suggestion.timestamp
        FROM suggestion
        LEFT JOIN response ON suggestion.id=suggestion_id
        GROUP BY suggestion.id
        HAVING COUNT(response.id)=0
        '''
    )


functions = OrderedDict([
    ('Filter Active Users', filter_active_users),
    ('Find User', find_user),
    ('Filter Suggestions With Contact Requests',
     filter_unconcacted_suggestors),
    ('Filter Suggestions Without Responses',
     filter_suggestions_without_responses)
])


if __name__ == '__main__':
    generate_ui(database, functions, input_prompt, again_prompt)
