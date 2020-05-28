import pytest

from anonymizer.mechanisms.suppression import Suppression, SuppressionParameters


@pytest.fixture()
def input_value():
    return "sEcReT"


def test_simple(input_value):
    mechanism = Suppression()
    assert mechanism.anonymize(input_value) == "XXXXXX"


def test_character(input_value):
    mechanism = Suppression(suppression_char=".")
    assert mechanism.anonymize(input_value) == "......"


def test_custom_len(input_value):
    mechanism = Suppression(custom_length=3)
    assert mechanism.anonymize(input_value) == "XXX"

    mechanism = Suppression(custom_length=lambda l: l // 2)
    assert mechanism.anonymize(input_value) == "XXX"


def test_combined(input_value):
    mechanism = Suppression(suppression_char=".", custom_length=3)
    assert mechanism.anonymize(input_value) == "..."


def test_parameters_model(input_value):
    parameters = SuppressionParameters(suppression_char=".")
    mechanism = Suppression(parameters=parameters)
    assert mechanism.anonymize(input_value) == "......"

    parameters = SuppressionParameters(custom_length=3)
    mechanism = Suppression(parameters=parameters)
    assert mechanism.anonymize(input_value) == "XXX"

    parameters = SuppressionParameters(custom_length=lambda l: l // 2)
    mechanism = Suppression(parameters=parameters)
    assert mechanism.anonymize(input_value) == "XXX"

    parameters = SuppressionParameters(custom_length=lambda l: l // 2)
    mechanism = parameters.build()
    assert mechanism.anonymize(input_value) == "XXX"
