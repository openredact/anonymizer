import pytest

from anonymizer.mechanisms.suppression import Suppression


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
