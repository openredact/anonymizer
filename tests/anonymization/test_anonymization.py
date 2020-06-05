import pytest

from anonymizer.anonymization.anonymizer import Anonymizer
from anonymizer.anonymization.config import AnonymizerConfig
from anonymizer.anonymization.pii import Pii, AnonymizedPii
from anonymizer.mechanisms.pseudonymization import PseudonymizationParameters
from anonymizer.mechanisms.stateful_mechanism import StatefulMechanismParameters
from anonymizer.mechanisms.suppression import SuppressionParameters


@pytest.fixture()
def piis():
    return [
        Pii("test", "Alpha", 0),
        Pii("foo", "Beta", 1),
        Pii("bar", "Gamma", 2),
        Pii("bar", "Gamma", 3),
    ]


def test_with_default(piis):
    config = AnonymizerConfig(
        default_mechanism=SuppressionParameters(),
        mechanisms_by_tag={
            "foo": SuppressionParameters(suppression_char="Y", custom_length=3),
            "bar": PseudonymizationParameters(format_string="Bar {}"),
        },
    )
    anonymizer = Anonymizer(config)

    anonymized_piis = [
        AnonymizedPii.from_pii(piis[0], "XXXXX"),
        AnonymizedPii.from_pii(piis[1], "YYY"),
        AnonymizedPii.from_pii(piis[2], "Bar 1"),
        AnonymizedPii.from_pii(piis[3], "Bar 2"),
    ]

    assert anonymizer.anonymize_individual(piis[0]) == anonymized_piis[0]
    assert anonymizer.anonymize(piis[0]) == anonymized_piis[0]

    assert list(anonymizer.anonymize(piis)) == anonymized_piis


def test_without_default(piis):
    # + stateful pseudonymization.
    config = AnonymizerConfig(
        mechanisms_by_tag={
            "foo": SuppressionParameters(suppression_char="Y", custom_length=3),
            "bar": StatefulMechanismParameters(mechanism_config=PseudonymizationParameters(format_string="Bar {}")),
        }
    )
    anonymizer = Anonymizer(config)

    anonymized_piis = [
        AnonymizedPii.from_pii(piis[0]),
        AnonymizedPii.from_pii(piis[1], "YYY"),
        AnonymizedPii.from_pii(piis[2], "Bar 1"),
        AnonymizedPii.from_pii(piis[3], "Bar 1"),
    ]

    assert anonymizer.anonymize_individual(piis[0]) == anonymized_piis[0]
    assert anonymizer.anonymize(piis[0]) == anonymized_piis[0]

    assert list(anonymizer.anonymize(piis)) == anonymized_piis
