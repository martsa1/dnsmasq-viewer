'''
Exceptions used throughout the backend library.
'''

class LeaseParseError(Exception):
    '''
    Used to signify that we were unable to locate a leases file to work with,
    or that we were unable to read or parse a file if we did find it.
    '''
    pass
