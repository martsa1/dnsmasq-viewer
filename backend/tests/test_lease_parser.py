'''
Unit Tests for the backend.lease_parser module.
'''

import builtins
from unittest.mock import mock_open, create_autospec

import pytest
import arrow
import netaddr

import backend.lease_parser as lp

from backend.exceptions import LeaseParseError
from backend.structures import LeaseRecord


def test_get_lease_file(monkeypatch):
    '''
    Verify we get a list of strings back from the
    backend.lease_parser.get_lease_file function when passed default or valid
    input.
    '''
    # Mock the file open stuff so it doesn't get in the way of testing...
    mock_string = 'some string'
    mocked_file = mock_open(read_data=mock_string)
    monkeypatch.setattr('builtins.open', mocked_file)

    lease_lines = lp.get_lease_file()

    assert lease_lines == [mock_string]


def test_get_lease_file_raises(monkeypatch):
    '''
    Verify we get a LeaseParseError when lp.get_lease_file can't open a file.
    '''
    # Mock the file open stuff so it doesn't get in the way of testing...
    mocked_file = mock_open()
    mocked_file.side_effect = IOError

    monkeypatch.setattr(builtins, 'open', mocked_file)

    with pytest.raises(LeaseParseError):
        lp.get_lease_file()
        print(mocked_file.call_args_list)


@pytest.mark.parametrize(
    'input_string,expected_result',
    [
        (
            '1535916991 aa:bb:cc:dd:ee:ff 172.16.1.60 android-2bfa2b2619add6eb 01:aa:bb:cc:dd:ee:ff',
            LeaseRecord(
                lease_expiry_time=arrow.get(1535916991),
                mac_address=netaddr.EUI('aa:bb:cc:dd:ee:ff'),
                ip_address=netaddr.IPAddress('172.16.1.60'),
                hostname='android-2bfa2b2619add6eb',
                client_id='01:aa:bb:cc:dd:ee:ff',
            )
        ),
        (
            '1535916891 aa:bb:cc:dd:ee:ff 172.16.1.220 * 01:aa:bb:cc:dd:ee:ff',
            LeaseRecord(
                lease_expiry_time=arrow.get(1535916891),
                mac_address=netaddr.EUI('aa:bb:cc:dd:ee:ff'),
                ip_address=netaddr.IPAddress('172.16.1.220'),
                hostname='',
                client_id='01:aa:bb:cc:dd:ee:ff',
            )
        ),
        (
            '1535966088 aa:bb:cc:dd:ee:ff 1.1.1.1 some-hostname *',
            LeaseRecord(
                lease_expiry_time=arrow.get(1535966088),
                mac_address=netaddr.EUI('aa:bb:cc:dd:ee:ff'),
                ip_address=netaddr.IPAddress('1.1.1.1'),
                hostname='some-hostname',
                client_id='',
            )
        ),
        (
            '1535966088 aa:bb:cc:dd:ee:ff 1.1.1.1 * *',
            LeaseRecord(
                lease_expiry_time=arrow.get(1535966088),
                mac_address=netaddr.EUI('aa:bb:cc:dd:ee:ff'),
                ip_address=netaddr.IPAddress('1.1.1.1'),
                hostname='',
                client_id='',
            )
        ),
    ]
)
def test_parse_lease(input_string: str, expected_result: object):
    '''
    Verify we get a LeaseRecord when parsing appropriate Lease strings.
    '''
    parsed_lease = lp.parse_lease(input_string)

    print('Expected Result: {},\nActual Result: {}'.format(str(expected_result), str(parsed_lease)))
    assert isinstance(parsed_lease, LeaseRecord)

    assert parsed_lease.lease_expiry_time == expected_result.lease_expiry_time
    assert parsed_lease.mac_address == expected_result.mac_address
    assert parsed_lease.ip_address == expected_result.ip_address
    assert parsed_lease.hostname == expected_result.hostname
    assert parsed_lease.client_id == expected_result.client_id


@pytest.mark.parametrize(
    'input_string,expected_error',
    [
        (
            '1535916991 aa:bb:cc:dd:ee:ff 1.2.3.a android-2bfa2b2619add6eb 01:aa:bb:cc:dd:ee:ff',
            LeaseParseError
        ),
        (
            '1535916891 aa:bb:cc:dd:ee:zz 1.1.1.1 * 01:aa:bb:cc:dd:ee:ff',
            LeaseParseError
        ),
        (
            '153596608a aa:bb:cc:dd:ee:ff 1.1.1.1 some-hostname *',
            LeaseParseError
        ),
        (
            'not-an-integer aa:bb:cc:dd:ee:ff 1.1.1.1 * *',
            LeaseParseError
        ),
        (
            '',  # Empty String should fail
            ValueError
        ),
        (
            123,  # Non-string should fail
            ValueError
        ),
    ]
)
def test_parse_lease_raises(input_string: str, expected_error: Exception):
    '''
    Verify we get a LeaseParseError when parsing a malformed DHCP Lease string
    '''
    with pytest.raises(expected_error):
        lp.parse_lease(input_string)
