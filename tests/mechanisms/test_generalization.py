from anonymizer.mechanisms.generalization import Generalization, GeneralizationParameters


def test_simple():
    mechanism = Generalization("<NAME>")
    assert mechanism.anonymize("Darth Vader") == "<NAME>"

    mechanism = Generalization(lambda x: x.split()[0] + " person")
    assert mechanism.anonymize("a woman") == "a person"


def test_parameters_model():
    mechanism = Generalization(GeneralizationParameters(replacement="<NAME>"))
    assert mechanism.anonymize("Darth Vader") == "<NAME>"

    mechanism = Generalization(GeneralizationParameters(replacement=lambda x: x.split()[0] + " person"))
    assert mechanism.anonymize("a woman") == "a person"
