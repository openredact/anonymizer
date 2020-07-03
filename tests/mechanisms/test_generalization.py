import pytest
from pydantic import ValidationError

from anonymizer.mechanisms.generalization import Generalization


def test_simple():
    mechanism = Generalization(replacement="<NAME>")
    assert mechanism.anonymize("Darth Vader") == "<NAME>"

    mechanism = Generalization(replacement=lambda x: x.split()[0] + " person")
    assert mechanism.anonymize("a woman") == "a person"


def test_invalid_arguments():
    with pytest.raises(ValidationError):
        Generalization()
