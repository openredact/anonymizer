import pytest

from anonymizer.mechanisms.suppression import Suppression


@pytest.fixture()
def input_value():
    return "sEcReT"


def test_rng():
    values = [3, 5, 7, 2, 1]
    i = 0

    def random(_):
        nonlocal i
        i = (i + 1) % len(values)
        return values[i]

    return random


def test_stateful(input_value):
    mechanism = Suppression(custom_length=test_rng(), stateful=False)
    # Normal suppression should return different outputs.
    assert mechanism.anonymize(input_value) != mechanism.anonymize(input_value)

    stateful_mechanism = Suppression(custom_length=test_rng(), stateful=True)
    # Stateful suppression should return same output.
    assert stateful_mechanism.anonymize(input_value) == stateful_mechanism.anonymize(input_value)
