import pytest

from anonymizer.mechanisms.pseudonymization import Pseudonymization


@pytest.fixture()
def input_value():
    return "sEcReT"


def test_simple(input_value):
    mechanism = Pseudonymization("Test ({})")
    assert mechanism.anonymize(input_value) == "Test (1)"
    assert mechanism.anonymize(input_value) == "Test (2)"


def test_initial_value(input_value):
    mechanism = Pseudonymization("Test ({})", initial_counter_value=0)
    assert mechanism.anonymize(input_value) == "Test (0)"
    assert mechanism.anonymize(input_value) == "Test (1)"
