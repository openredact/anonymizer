import pytest
from pydantic import ValidationError

from anonymizer.mechanisms.pseudonymization import Pseudonymization


@pytest.fixture()
def input_value():
    return "sEcReT"


def test_simple(input_value):
    mechanism = Pseudonymization(format_string="Test ({})")
    assert mechanism.anonymize(input_value) == "Test (1)"
    assert mechanism.anonymize(input_value) == "Test (2)"


def test_initial_value(input_value):
    mechanism = Pseudonymization(format_string="Test ({})", counter=0)
    assert mechanism.anonymize(input_value) == "Test (0)"
    assert mechanism.anonymize(input_value) == "Test (1)"


def test_invalid_arguments(input_value):
    with pytest.raises(ValidationError):
        Pseudonymization()
