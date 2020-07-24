from typing import Union

from .generalization import GeneralizationParameters, Generalization
from .laplace_noise import LaplaceNoise, LaplaceNoiseParameters
from .pseudonymization import PseudonymizationParameters, Pseudonymization
from .randomized_response import RandomizedResponseParameters, RandomizedResponse
from .suppression import SuppressionParameters, Suppression


def mechanism_types():
    return Union[Generalization, Pseudonymization, Suppression, RandomizedResponse, LaplaceNoise]


def mechanism_config_types():
    return Union[
        GeneralizationParameters,
        PseudonymizationParameters,
        SuppressionParameters,
        RandomizedResponseParameters,
        LaplaceNoiseParameters,
    ]


def is_config(v):
    return isinstance(
        v,
        (
            GeneralizationParameters,
            PseudonymizationParameters,
            SuppressionParameters,
            RandomizedResponseParameters,
            LaplaceNoiseParameters,
        ),
    )
