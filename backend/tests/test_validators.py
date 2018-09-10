'''
Unit Tests for the backend.validators module.
'''

import pytest
import arrow

from apistar.exceptions import ValidationError
from netaddr import IPAddress, EUI

import backend.validators as bv


@pytest.mark.parametrize(
    'input_, allow_null, allow_coerce, format_str, expected_output',
    [
        # allow_coerce tests
        (0, False, True, None, arrow.get(0)),
        (arrow.get(0), False, True, None, arrow.get(0)),

        # Format String coercions
        ('1900/01/01', False, True, 'YYYY/MM/DD', arrow.get(1900, 1, 1)),
        ('01/04/2018', False, True, 'DD/MM/YYYY', arrow.get(2018, 4, 1)),

        # None tests
        (None, True, True, None, None),
        (None, True, False, None, None),
        ('', True, False, None, None),
    ]
)
def test_arrow_validator_validate(input_, allow_null, allow_coerce, format_str, expected_output):
    '''
    Verify we can put a number of values in and get arrow types back out.
    '''
    validator = bv.ArrowValidator(allow_null=allow_null, format_str=format_str)

    assert validator.validate(
        input_,
        allow_coerce=allow_coerce,
    ) == expected_output


@pytest.mark.parametrize(
    'input_, allow_null, allow_coerce, format_str',
    [
        # Improper Datetimes
        ('abc', False, False, None),
        ('abc', False, True, None),
        ('aa/bl/ah', False, False, None),
        ('aa/bl/ah', False, True, None),

        ('aa/bl/ah', False, False, 'dd/mm/yyyy/'),
        ('aa/bl/ah', False, True, 'dd/mm/yyyy/'),

        # None tests
        (None, False, True, None),
        (None, False, False, None),
        ('', False, False, None),
        ('none', False, False, None),
    ]
)
def test_arrow_validator_raises(input_, allow_null, allow_coerce, format_str):
    '''
    Verify we can see appropriate errors for various error cases with the ArrowValidator class.
    '''
    validator = bv.ArrowValidator(allow_null=allow_null, format_str=format_str)

    with pytest.raises(ValidationError):
        validator.validate(input_, allow_coerce=allow_coerce)


def test_arrow_validator_asserts():
    '''
    Verify that a non-string format_str will raise an assertion error.
    '''
    with pytest.raises(AssertionError):
        bv.ArrowValidator(format_str=1)


###################################################################################################


@pytest.mark.parametrize(
    'input_, allow_null, allow_coerce, version, expected_output',
    [
        # allow_coerce tests
        (0, False, True, None, IPAddress(0)),
        (IPAddress(0), False, True, None, IPAddress(0)),

        # version tests
        ('1.2.3.4', False, True, 4, IPAddress('1.2.3.4', 4)),
        ('::', False, True, 6, IPAddress('::', 6)),

        # None tests
        (None, True, True, None, None),
        (None, True, False, None, None),
        ('', True, False, None, None),
    ]
)
def test_ip_address_validator_validate(input_, allow_null, allow_coerce, version, expected_output):
    '''
    Verify we can put a number of values in and get arrow types back out.
    '''
    validator = bv.IPAddressValidator(allow_null=allow_null, version=version)

    assert validator.validate(
        input_,
        allow_coerce=allow_coerce,
    ) == expected_output


@pytest.mark.parametrize(
    'input_, allow_null, allow_coerce, version',
    [
        # Improper IP Addresses
        ('abc', False, False, None),
        ('abc', False, True, None),
        ('abc', True, True, None),

        # Incorrect IP Address versions
        ('::', False, True, 4),
        ('1.2.3.4', False, True, 6),

        # None tests
        (None, False, True, None),
        (None, False, False, None),
        ('', False, False, None),
        ('none', False, False, None),
    ]
)
def test_ip_address_validator_raises(input_, allow_null, allow_coerce, version):
    '''
    Verify we can see appropriate errors for various error cases with the
    IPAddressValidator class.
    '''
    validator = bv.IPAddressValidator(allow_null=allow_null, version=version)

    with pytest.raises(ValidationError):
        validator.validate(input_, allow_coerce=allow_coerce)


def test_ip_address_validator_asserts():
    '''
    Verify that a non-string format_str will raise an assertion error.
    '''
    with pytest.raises(AssertionError):
        bv.IPAddressValidator(version='thing')


###################################################################################################


@pytest.mark.parametrize(
    'input_, allow_null, allow_coerce, version, expected_output',
    [
        # allow_coerce tests
        (0, False, True, None, EUI(0)),
        (EUI(0), False, True, None, EUI(0)),

        # version tests
        ('11-22-33-44-55-66', False, True, 48, EUI('11-22-33-44-55-66')),
        ('00-00-00-00-00-00-00-01', False, True, 64, EUI('00-00-00-00-00-00-00-01')),

        # None tests
        (None, True, True, None, None),
        (None, True, False, None, None),
        ('', True, False, None, None),
    ]
)
def test_eui_validator_validate(input_, allow_null, allow_coerce, version, expected_output):
    '''
    Verify we can put a number of values in and get EUI types back out.
    '''
    validator = bv.MACValidator(allow_null=allow_null, version=version)

    assert validator.validate(
        input_,
        allow_coerce=allow_coerce,
    ) == expected_output


@pytest.mark.parametrize(
    'input_, allow_null, allow_coerce, version',
    [
        # Improper MAC Addresses
        ('abc', False, False, None),
        ('abc', False, True, None),
        ('abc', True, True, None),

        # Incorrect MAC Address versions
        ('00-00-00-00-00-00-00-01', False, True, 48),
        ('11-22-33-44-55-66', False, True, 64),

        # None tests
        (None, False, True, None),
        (None, False, False, None),
        ('', False, False, None),
        ('none', False, False, None),
    ]
)
def test_eui_validator_raises(input_, allow_null, allow_coerce, version):
    '''
    Verify we can see appropriate errors for various error cases with the MACValidator class.
    '''
    validator = bv.MACValidator(allow_null=allow_null, version=version)

    with pytest.raises(ValidationError):
        validator.validate(input_, allow_coerce=allow_coerce)


def test_eui_validator_asserts():
    '''
    Verify that a non-string version, or one out of range will raise an assertion error.
    '''
    with pytest.raises(AssertionError):
        bv.MACValidator(version='thing')

    with pytest.raises(AssertionError):
        bv.MACValidator(version=50)
