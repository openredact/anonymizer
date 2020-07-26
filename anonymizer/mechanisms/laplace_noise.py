import numpy as np
from pydantic.types import constr, PositiveFloat

from .encoding_mechanism import EncodingMechanism
from ..utils.pydantic_base_model import CamelBaseModel


class LaplaceNoise(EncodingMechanism):
    """
    The laplace noise mechanisms anonymizes input by perturbing it using the laplace distribution.
    While this approach is similar to noising results using the laplace mechanism for Differential Privacy,
    using our laplace noise mechanism itself does not provide any Differential Privacy guarantees per se.

    This mechanisms takes one mandatory parameter `epsilon`, which influences the amount of noise added
    (smaller epsilon means more noise).

    The optional parameter `sensitivity` is also used to scale the noise (larger sensitivity means more noise).

    >>> mechanism = LaplaceNoise(epsilon=10000000000)
    >>> assert abs(mechanism.anonymize(1.5) - 1.5) < 0.1  # with high probability
    """

    epsilon: PositiveFloat
    sensitivity: PositiveFloat = 1.0

    def apply(self, input_value):
        """
        Anonymizes the given input parameter.
        If the input_value is not a number, it raises a ValueError.
        """
        input_value = float(input_value)
        noise = np.random.laplace(scale=self.sensitivity / self.epsilon)
        return input_value + noise


class LaplaceNoiseParameters(CamelBaseModel):
    mechanism: constr(regex="^laplaceNoise$") = "laplaceNoise"
    config: LaplaceNoise
