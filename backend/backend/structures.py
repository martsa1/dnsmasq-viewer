'''
Various data container classes used throughout the backend service.
'''

import attr

@attr.s
class LeaseRecord():
    '''
    Data container used to store the various bits of a DHCP Lease.

    1535916991 f4:f5:24:8a:46:3a 172.16.1.60 android-2bfa2b2619add6eb 01:f4:f5:24:8a:46:3a
    Format of above line: lease expiry time, mac address, ip address, hostname, client id
    '''
    ip_address = attr.ib()
    mac_address = attr.ib()
    lease_expiry_time = attr.ib()

    client_id = attr.ib('')
    hostname = attr.ib('')
