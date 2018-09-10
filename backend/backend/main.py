'''
Entrypoints for the backend API Server.
'''

from backend.api.api import APP


def main():
    ''' Default entrypoint for the backend server.
    '''
    APP.serve('0.0.0.0', 5000, debug=True)
