from typing import Union

from .generalization import GeneralizationParameters, Generalization
from .pseudonymization import PseudonymizationParameters, Pseudonymization
from .randomized_response import RandomizedResponseParameters, RandomizedResponse
from .suppression import SuppressionParameters, Suppression


def mechanism_types():
    return Union[Generalization, Pseudonymization, Suppression, RandomizedResponse]


def mechanism_config_types():
    return Union[GeneralizationParameters, PseudonymizationParameters, SuppressionParameters, RandomizedResponseParameters]


def is_config(v):
    return isinstance(
        v, (GeneralizationParameters, PseudonymizationParameters, SuppressionParameters, RandomizedResponseParameters)
    )
