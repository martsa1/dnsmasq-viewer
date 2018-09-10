'''
APIStar module to present an OpenAPI v3 compliant rest interface on top of the
DNS Masq DHCP lease file.
'''

import typing
from os.path import dirname, join

from apistar import App, Route

from backend.validators import LeaseRecord
from backend.lease_parser import parse_lease, get_lease_file


def leases() -> typing.List[LeaseRecord]:
    '''
    Return a list of JSON LeaseRecord's.
    '''
    lease_records = [
        parse_lease(lease).serialise()
        for lease in get_lease_file(
            join(
                dirname(__file__),
                '../../static/leasefile'
            )
        )
    ]
    return lease_records


ROUTES = [
    Route('/leases/', method='GET', handler=leases),
]

APP = App(routes=ROUTES)
