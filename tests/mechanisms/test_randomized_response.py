from anonymizer.mechanisms.randomized_response import RandomizedResponse


def test_simple():
    # Always return true answer.
    mechanism = RandomizedResponse(["Yes", "No"], probability_distribution=[[1, 0], [0, 1]])
    assert mechanism.anonymize("No") == "No"
    assert mechanism.anonymize("Yes") == "Yes"
    thrown = False
    try:
        mechanism.anonymize("Foobar")
    except ValueError:
        thrown = True
    assert thrown

    # Mismatch between distribution and values.
    thrown = False
    try:
        mechanism = RandomizedResponse(["Yes"], probability_distribution=[[1, 0], [0, 1]])
    except ValueError:
        thrown = True
    assert thrown


def test_coin():
    # Always return true answer.
    mechanism = RandomizedResponse.with_coin(["Yes", "No"], coin_p=1, default_value="<None>")
    assert mechanism.anonymize("Yes") == "Yes"
    assert mechanism.anonymize("No") == "No"
    assert mechanism.anonymize("Foobar") == "<None>"

    # Throw error.
    mechanism = RandomizedResponse.with_coin(["Yes", "No"], coin_p=1)
    thrown = False
    try:
        mechanism.anonymize("Foobar")
    except ValueError:
        thrown = True
    assert thrown

    # Always return other answer.
    weights = [[0, 1], [1, 0]]
    mechanism = RandomizedResponse.with_coin(["Yes", "No"], coin_p=0, probability_distribution=weights)
    assert mechanism.anonymize("Yes") == "No"
    assert mechanism.anonymize("No") == "Yes"


def test_dp():
    # Return true answer with very high probability.
    # The true answer has a weight of 1.0, while the wrong answer has a weight of ~3e-44.
    mechanism = RandomizedResponse.with_dp(["Yes", "No"], 100)
    assert mechanism.anonymize("Yes") == "Yes"
    assert mechanism.anonymize("No") == "No"

    # Throw error.
    mechanism = RandomizedResponse.with_coin(["Yes", "No"], coin_p=1)
    thrown = False
    try:
        mechanism.anonymize("Foobar")
    except ValueError:
        thrown = True
    assert thrown

    # Always return other answer.
    weights = [[0, 1], [1, 0]]
    mechanism = RandomizedResponse.with_coin(["Yes", "No"], coin_p=0, probability_distribution=weights)
    assert mechanism.anonymize("Yes") == "No"
    assert mechanism.anonymize("No") == "Yes"
