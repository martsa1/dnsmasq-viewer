'''
Methods involved in parsing the DNS Masq Lease file
'''

import logging
from typing import Union

import arrow

from arrow.parser import ParserError
from netaddr import IPAddress, EUI
from netaddr.core import AddrFormatError

from backend.exceptions import LeaseParseError
from backend.validators import LeaseRecord


LOG = logging.getLogger(__name__)


def get_lease_file(path: str = None) -> Union[list, None]:
    '''
    Simple function to return the text from a lease file.

    :path: str: if provided, attempt to open an absolute path to a DNS Masq
    Lease file.

    If path is not provided, the function will look in one of two places:
     -  /var/lib/misc/dnsmasq.leases
     -  /etc/dnsmasq.d/dnsmasq.leases

    :returns List: Returns a list of lease strings, ready to be parsed.
    :raises LeasesNotFoundError: Function will raise a LeasesNotFoundError if
    path or neither of the defaults correctly loads a file.
    '''
    files_to_try = [
        '/var/lib/misc/dnsmasq.leases',
        '/etc/dnsmasq.d/dnsmasq.leases'
    ]

    if path and isinstance(path, str):
        files_to_try.insert(0, path)

    for file in files_to_try:
        try:
            print('Pre open')
            with open(file, 'r') as file_handle:
                print('inside open')
                file_contents = file_handle.readlines()
                return file_contents
        except IOError:
            print('inside IOError')
            # If we don't find a file, or for whatever reason can't open it,
            # try the next file in the list.
            continue

    # If we get here, we've exhausted our set of files to try and open, so we
    # raise a LeasesNotFoundError.
    print('Raising LeaseParseError')
    raise LeaseParseError


def parse_lease(lease_line: str) -> Union[LeaseRecord, None]:
    '''
    Parse a string representing a DNS Masq DHCP Lease.

    :lease_line: str: a string representing a DHCP lease from DNS Masq's leases file

    :raises LeaseParseError: if unable to correctly parse a DHCP lease.
    :returns LeaseRecord: Data structure representing a DHCP lease.
    '''
    if not lease_line or not isinstance(lease_line, str):
        raise ValueError('Must provide a string input')

    print('Processing: {},\n{}'.format(lease_line, lease_line.split(' ')))
    #  LOG.debug('Processing: %s', lease_line)

    #  Format of lease line: lease expiry time, mac_address, ip address,
    #  hostname, client id
    expiry_time, mac_address, ip_address, hostname, client_id = lease_line.strip().split(' ')
    try:
        ip_address = IPAddress(ip_address)
        mac_address = EUI(mac_address)
    except (AttributeError, AddrFormatError):
        raise LeaseParseError(
            'Unable to parse IP or Mac address in {}'.format(lease_line)
        )

    try:
        expiry_time = arrow.get(expiry_time)
    except (ValueError, ParserError):
        raise LeaseParseError('Unable to parse lease expiry time')

    # DHCP lease isn't associated with a hostname
    hostname = '' if hostname == '*' else hostname

    # DHCP lease isn't associated with a client ID
    client_id = '' if client_id == '*' else client_id

    return LeaseRecord(
        client_id=client_id,
        hostname=hostname,
        ip_address=ip_address,
        lease_expiry_time=expiry_time,
        mac_address=mac_address,
    )
