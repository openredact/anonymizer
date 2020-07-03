import pytest
from pydantic import ValidationError

from anonymizer.mechanisms.randomized_response import RandomizedResponse, RandomizedResponseMode


def test_simple():
    # Always return true answer.
    mechanism = RandomizedResponse(values=["Yes", "No"], probability_distribution=[[1, 0], [0, 1]])
    assert mechanism.anonymize("No") == "No"
    assert mechanism.anonymize("Yes") == "Yes"
    with pytest.raises(ValueError):
        mechanism.anonymize("Foobar")

    # Mismatch between distribution and values.
    with pytest.raises(ValidationError):
        RandomizedResponse(values=["Yes"], probability_distribution=[[1, 0], [0, 1]])


def test_coin():
    # Always return true answer.
    mechanism = RandomizedResponse(values=["Yes", "No"], coin_p=1, default_value="<None>", mode=RandomizedResponseMode.coin)
    assert mechanism.anonymize("Yes") == "Yes"
    assert mechanism.anonymize("No") == "No"
    assert mechanism.anonymize("Foobar") == "<None>"

    # Throw error.
    mechanism = RandomizedResponse(values=["Yes", "No"], coin_p=1, mode=RandomizedResponseMode.coin)
    with pytest.raises(ValueError):
        mechanism.anonymize("Foobar")

    # Always return other answer.
    weights = [[0, 1], [1, 0]]
    mechanism = RandomizedResponse(
        values=["Yes", "No"], coin_p=0, probability_distribution=weights, mode=RandomizedResponseMode.coin
    )
    assert mechanism.anonymize("Yes") == "No"
    assert mechanism.anonymize("No") == "Yes"


def test_dp():
    # Return true answer with very high probability.
    # The true answer has a weight of 1.0, while the wrong answer has a weight of ~3e-44.
    mechanism = RandomizedResponse(values=["Yes", "No"], epsilon=100, mode=RandomizedResponseMode.dp)
    assert mechanism.anonymize("Yes") == "Yes"
    assert mechanism.anonymize("No") == "No"
