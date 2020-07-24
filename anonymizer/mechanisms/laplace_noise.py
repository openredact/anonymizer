import numpy as np
from pydantic.types import constr, PositiveFloat

from .stateful_mechanism import StatefulMechanism
from ..utils.pydantic_base_model import CamelBaseModel


class LaplaceNoise(StatefulMechanism):
    """
    The laplace noise mechanisms anonymizes input by perturbing it using the laplace distribution.
    While this approach is similar to noising results using the laplace mechanism for Differential Privacy,
    using our laplace noise mechanism itself does not provide any Differential Privacy guarantees per se.

    This mechanisms takes one mandatory parameter `epsilon`, which influences the amount of noise added
    (smaller epsilon means more noise).

    The optional parameter `sensitivity` is also used to scale the noise (larger sensitivity means more noise).

    >>> mechanism = LaplaceNoise(values=['Yes', 'No'], probability_distribution=[1, 0])
    >>> mechanism.anonymize('Yes')
    'Yes'
    >>> mechanism.anonymize('No')
    'Yes'

    The mechanisms allows to specify a third, optional parameter `default_value`.
    This mechanism usually requires the list of `values` to be exhaustive over all possible inputs.
    If `anonymize` is called with an unknown value, this mechanism may raise a ValueError.
    Specifying the `default_value` prevents this and returns the `default_value` in such cases.

    >>> mechanism = RandomizedResponse(values=['Yes', 'No'], probability_distribution=[0, 1], default_value='<UNKNOWN>')
    >>> mechanism.anonymize('Yes')
    'No'
    >>> mechanism.anonymize('Foobar')
    '<UNKNOWN>'
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
