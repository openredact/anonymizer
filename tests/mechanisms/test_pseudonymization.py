import pytest
from pydantic import ValidationError

from anonymizer.mechanisms.pseudonymization import Pseudonymization, PseudonymizationParameters


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


def test_parameters_model(input_value):
    mechanism = Pseudonymization(PseudonymizationParameters(format_string="Test ({})", initial_counter_value=0))
    assert mechanism.anonymize(input_value) == "Test (0)"
    assert mechanism.anonymize(input_value) == "Test (1)"

    with pytest.raises(ValidationError):
        PseudonymizationParameters(format_string="Test")
