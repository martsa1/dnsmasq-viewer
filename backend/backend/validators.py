'''
Various data container classes used throughout the backend service.
'''

import logging

from datetime import datetime, date

import arrow

from apistar import types, validators
from netaddr import AddrFormatError, EUI, IPAddress

LOG = logging.getLogger(__name__)


class ArrowValidator(validators.Validator):
    '''
    Type validator for arrow type data.  Allows API Star to validate Arrow type data.

    Arrow types are much more better than native dateTimes...!

    Structure of this class is inspired by APIStar's builtin validators, source
    is here:
    https://github.com/encode/apistar/blob/master/apistar/validators.py
    '''
    errors = {
        'type': 'Must be a valid Arrow Type',
        'parse': 'Must be a parsable string or number that can be interpreted'
                 ' by arrow.get()',
        'null': 'May not be null'
    }

    null_values = [
        None,
        '',
        'null',
        'none',
    ]

    def __init__(self, format_str=None, **kwargs):
        super().__init__(**kwargs)

        LOG.debug('Verifying type of format_str')
        assert format_str is None or isinstance(format_str, str)

        self.format_str = format_str

    def validate(self, value, definitions=None, allow_coerce=False):
        ''' Default method to provide Arrow type validation of provided input.'''
        LOG.debug(
            'Validating: %s, definitions: %s, allow_coerce: %s',
            value,
            definitions,
            allow_coerce
        )
        for example in self.null_values:
            if value == example:
                if self.allow_null:
                    LOG.debug('Value was none and was allowed, returning None')
                    return None

                LOG.debug("Value was none and isn't allowed, raising")
                self.error('null')

        if not isinstance(value, arrow.Arrow):
            LOG.debug(
                'Value isn\'t an Arrow type: %s, allow_coerce: %s',
                type(value),
                allow_coerce
            )
            if allow_coerce and isinstance(value, (str, int, float, date, datetime)):
                LOG.debug('Attempting to convert value to Arrow Type.')
                try:
                    if self.format_str:
                        LOG.debug(
                            'Attempting to convert using format_str: %s',
                            self.format_str
                        )
                        result = arrow.get(value, self.format_str)
                        LOG.debug('Successfully coerced to Arrow type: %s', result)
                        return result

                    result = arrow.get(value)
                    LOG.debug('Successfully coerced to Arrow type: %s', result)
                    return result

                except arrow.parser.ParserError:
                    LOG.debug('Failed to parse value into Arrow type.')

            self.error('parse')

        return value


class IPAddressValidator(validators.Validator):
    '''
    Type validator for IPAddress type data.  Allows API Star to validate IPAddress type data.

    Allows us to use netaddr.IPAddress data types and validate them appropriately.

    Structure of this class is inspired by APIStar's builtin validators, source
    is here:
    https://github.com/encode/apistar/blob/master/apistar/validators.py
    '''
    errors = {
        'type': 'Must be a valid IPAddress Type',
        'parse': 'Must be a parsable string or number that can be interpreted'
                 ' by netaddr.IPAddress()',
        'null': 'May not be null'
    }

    null_values = [
        None,
        '',
        'null',
        'none',
    ]

    def __init__(self, version=None, **kwargs):
        super().__init__(**kwargs)

        LOG.debug('Verifying type of version')
        assert version is None or (isinstance(version, int) and version in [4, 6])

        self.version = version

    def validate(self, value, definitions=None, allow_coerce=False):
        ''' Default method to provide IPAddress type validation of provided input.'''
        LOG.debug(
            'Validating: %s, definitions: %s, allow_coerce: %s, version: %s',
            value,
            definitions,
            allow_coerce,
            self.version
        )
        for example in self.null_values:
            if value == example:
                if self.allow_null:
                    LOG.debug('Value was none and was allowed, returning None')
                    return None

                LOG.debug("Value was none and isn't allowed, raising")
                self.error('null')

        if not isinstance(value, IPAddress):
            LOG.debug(
                'Value isn\'t an IPAddress type: %s, allow_coerce: %s',
                type(value),
                allow_coerce
            )
            if allow_coerce and isinstance(value, (str, int)):
                LOG.debug('Attempting to convert value to IPAddress Type.')
                try:
                    if self.version:
                        LOG.debug(
                            'Attempting to convert using version: %s',
                            self.version
                        )
                        result = IPAddress(value, self.version)
                        LOG.debug('Successfully coerced to IPAddress type: %s', result)
                        return result

                    result = IPAddress(value)
                    LOG.debug('Successfully coerced to IPAddress type: %s', result)
                    return result

                except AddrFormatError:
                    LOG.debug('Failed to parse value into IPAddress type.')

            self.error('parse')

        return value


class MACValidator(validators.Validator):
    '''
    Type validator for EUI (MAC Address) type data.  Allows API Star to
    validate IPAddress type data.

    Allows us to use netaddr.EUI data types and validate them appropriately.

    Structure of this class is inspired by APIStar's builtin validators, source
    is here:
    https://github.com/encode/apistar/blob/master/apistar/validators.py
    '''
    errors = {
        'type': 'Must be a valid EUI Type',
        'parse': 'Must be a parsable string or number that can be interpreted'
                 ' by netaddr.EUI()',
        'null': 'May not be null'
    }

    null_values = [
        None,
        '',
        'null',
        'none',
    ]

    def __init__(self, version=None, **kwargs):
        super().__init__(**kwargs)

        LOG.debug('Verifying type of version')
        assert version is None or (isinstance(version, int) and version in [48, 64])

        self.version = version

    def validate(self, value, definitions=None, allow_coerce=False):
        ''' Default method to provide EUI type validation of provided input.'''
        LOG.debug(
            'Validating: %s, definitions: %s, allow_coerce: %s, version: %s',
            value,
            definitions,
            allow_coerce,
            self.version
        )

        for example in self.null_values:
            if value == example:
                if self.allow_null:
                    LOG.debug('Value was none and was allowed, returning None')
                    return None

                LOG.debug("Value was none and isn't allowed, raising")
                self.error('null')

        if not isinstance(value, EUI):
            LOG.debug(
                'Value isn\'t an EUI type: %s, allow_coerce: %s',
                type(value),
                allow_coerce
            )
            if allow_coerce and isinstance(value, (str, int)):
                LOG.debug('Attempting to convert value to EUI Type.')
                try:
                    if self.version:
                        LOG.debug(
                            'Attempting to convert using version: %s', self.version
                        )
                        result = EUI(value, self.version)
                        LOG.debug('Successfully coerced to EUI type: %s', result)
                        return result

                    result = EUI(value)
                    LOG.debug('Successfully coerced to EUI type: %s', result)
                    return result

                except AddrFormatError:
                    LOG.debug('Failed to parse value into IPAddress type.')

            self.error('parse')

        return value


class LeaseRecord(types.Type):
    '''
    Data container used to store the various bits of a DHCP Lease.

    1535916991 f4:f5:24:8a:46:3a 172.16.1.60 android-2bfa2b2619add6eb 01:f4:f5:24:8a:46:3a
    Format of above line: lease expiry time, mac address, ip address, hostname, client id
    '''
    ip_address = IPAddressValidator()
    mac_address = MACValidator()
    lease_expiry_time = ArrowValidator()

    client_id = validators.String(default='')
    hostname = validators.String(default='')

    def serialise(self):
        '''
        Return JSON-able version of the LeaseRecord.
        '''
        serialised = dict(
            ip_address=str(self.ip_address),
            mac_address=str(self.mac_address),
            lease_expiry_time=str(self.lease_expiry_time),
            client_id=self.client_id,
            hostname=self.hostname,
        )

        return serialised
