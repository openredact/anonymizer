import pytest

from anonymizer.mechanisms.suppression import Suppression, SuppressionParameters
from anonymizer.mechanisms.stateful_mechanism import StatefulMechanism, StatefulMechanismParameters


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
    mechanism = Suppression(custom_length=test_rng())
    # Normal suppression should return different outputs.
    assert mechanism.anonymize(input_value) != mechanism.anonymize(input_value)

    stateful_mechanism = StatefulMechanism(mechanism)
    # Stateful suppression should return same output.
    assert stateful_mechanism.anonymize(input_value) == stateful_mechanism.anonymize(input_value)


def test_parameters_model():
    parameters = StatefulMechanismParameters(
        mechanism_config=SuppressionParameters(custom_length=test_rng(), suppression_char="Y")
    )
    mechanism = parameters.build()
    assert mechanism.anonymize("Darth Vader 1") != mechanism.anonymize("Darth Vader 2")
    assert mechanism.anonymize("Darth Vader 1") == mechanism.anonymize("Darth Vader 1")
