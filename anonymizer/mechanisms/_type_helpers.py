from typing import Union

from .generalization import GeneralizationParameters
from .pseudonymization import PseudonymizationParameters
from .randomized_response import RandomizedResponseParameters
from .suppression import SuppressionParameters


def mechanism_config_types():
    return Union[GeneralizationParameters, PseudonymizationParameters, SuppressionParameters, RandomizedResponseParameters]
