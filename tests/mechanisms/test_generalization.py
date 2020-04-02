from anonymizer.mechanisms.generalization import Generalization


def test_simple():
    mechanism = Generalization("<NAME>")
    assert mechanism.anonymize("Darth Vader") == "<NAME>"

    mechanism = Generalization(lambda x: x.split()[0] + " person")
    assert mechanism.anonymize("a woman") == "a person"
