import math
from enum import Enum

from pydantic import validator, Field
from typing import List, Optional, Union, Any
import numpy as np
from pydantic.types import constr

from anonymizer.utils.discrete_distribution import DiscreteDistribution
from .stateful_mechanism import StatefulMechanism
from ..utils.pydantic_base_model import CamelBaseModel


class RandomizedResponseMode(str, Enum):
    custom = "custom"
    coin = "coin"
    dp = "dp"


class RandomizedResponse(StatefulMechanism):
    """
    The randomized response mechanisms anonymizes input by replacing it with a certain probability
    with a value drawn from a given probability distribution.

    See: "Using Randomized Response for Differential Privacy Preserving Data Collection" by Wang, Wu, and Hu
    http://csce.uark.edu/~xintaowu/publ/DPL-2014-003.pdf
    Section 4: POLYCHOTOMOUS ATTRIBUTE

    This mechanisms takes two mandatory parameters: `values` and `probability_distribution`.

    The `values` parameter defines the list of potential replacements to select from.
    The `probability_distribution` parameter can be either of the following three:
    1) An instance of `DiscreteDistribution`,
    2) A list of weights with `len(probability_distribution) == len(values)`,
    3) A matrix where each row represents the list of weights for an input value,
       i.e., `probability_distribution[i][j]` is the probability of outputting value j given value i as an input.
       The dimensions of the matrix are `len(values) x len(values)`.

    >>> mechanism = RandomizedResponse(values=['Yes', 'No'], probability_distribution=[1, 0])
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

    MECHANISM: constr(regex="^randomizedResponse$") = "randomizedResponse"
    values: List[str]
    mode: RandomizedResponseMode = RandomizedResponseMode.custom
    # RandomizedResponseMode.{custom, coin}:
    probability_distribution: Optional[Union[List[float], List[List[float]], DiscreteDistribution]] = None
    epsilon: Optional[float] = None  # Only used for RandomizedResponseMode.dp
    coin_p: Optional[float] = None  # Only used for RandomizedResponseMode.coin
    default_value: Optional[str] = None
    cum_distr: Any = Field(default=None, const=True)

    @validator("probability_distribution", always=True)
    def distribution_size_matches(cls, v, values, **kwargs):
        if "values" not in values:
            raise ValueError("Missing required property: values")
        mode = values["mode"]
        if mode in (RandomizedResponseMode.custom, RandomizedResponseMode.coin):
            # Allow None in coin mode.
            if mode == RandomizedResponseMode.coin and v is None:
                return None
            num_probabilities = len(v)

            # For lists, we need to ensure they have the right shape.
            if isinstance(v, list):
                is_matrix = any([isinstance(row, list) for row in v])
                if num_probabilities == 0 or (
                    is_matrix and any([not isinstance(row, list) or len(row) != num_probabilities for row in v])
                ):
                    raise ValueError("Size of weights must not be 0 and must be a list or square matrix")

            if num_probabilities != len(values["values"]):
                raise ValueError("Size of probability distribution does not match values")
            return v
        else:
            return None

    @validator("epsilon", always=True)
    def epsilon_check(cls, v, values, **kwargs):
        mode = values["mode"]
        if mode == RandomizedResponseMode.dp:
            if v is None:
                raise ValueError("DP mode requires epsilon value")
            return v
        else:
            return None

    @validator("coin_p", always=True)
    def coin_p_check(cls, v, values, **kwargs):
        mode = values["mode"]
        if mode == RandomizedResponseMode.coin:
            if v is None:
                raise ValueError("Coin mode requires coin_p value")
            return v
        else:
            return None

    class Config:
        # Make sure conditional requirements are adequately reflected.
        schema_extra = {
            "anyOf": [
                {"properties": {"mode": {"const": "custom"}}, "required": ["probabilityDistribution"]},
                {"properties": {"mode": {"const": "dp"}}, "required": ["epsilon"]},
                {"properties": {"mode": {"const": "coin"}}, "required": ["coinP"]},
            ]
        }

    def __init__(self, **kwargs):
        """
        Initiates the randomized response mechanism.
        """
        super().__init__(**kwargs)

        # Build DiscreteDistribution object.
        distribution = (
            self.probability_distribution
            if self.probability_distribution is None or isinstance(self.probability_distribution, DiscreteDistribution)
            else DiscreteDistribution(self.probability_distribution)
        )

        # Create the cumulative probability distribution from the model.
        if self.mode == RandomizedResponseMode.dp:
            distribution = RandomizedResponse.__with_dp(len(self.values), self.epsilon)
        elif self.mode == RandomizedResponseMode.coin:
            distribution = RandomizedResponse.__with_coin(len(self.values), self.coin_p, distribution)

        # `distribution` cannot be None at this point if the model was validated.
        self.cum_distr = distribution.to_cumulative()

    @classmethod
    def __with_dp(cls, t, epsilon):
        """
        Calculates the distribution for a DP mechanisms with `t` values and the privacy parameter `epsilon`.

        Let `t = len(values)`.
        This results in a probability of `e^epsilon / (t - 1 + e^epsilon) for revealing the true value,
        and a probability of `1 / (t - 1 + e^epsilon)` for each other value.
        """
        e_eps = math.exp(epsilon)
        denominator = t - 1 + e_eps
        p_ii = e_eps / denominator
        p_ij = 1 / denominator

        # Create a matrix filled with p_ij
        weights = np.full((t, t), p_ij)
        # Create a matrix with diagonal entries p_ii - p_ij
        diag = np.zeros((t, t))
        np.fill_diagonal(diag, p_ii - p_ij)
        # Sum the two matrices to obtain our result
        weights += diag
        d = DiscreteDistribution(weights)
        return d

    @classmethod
    def __with_coin(cls, num_values, coin_p=0.5, probability_distribution=None):
        """
        Calculates the distribution for a mechanism that simulates the following experiment:
        1) Toss a coin (with heads having a probability `coin_p`, which defaults to 0.5).
        2) If heads, report true value.
        3) If tails, then throw another coin to randomly choose one element from `values`
           based on the `probability_distribution` (default is a uniform distribution).
           The probability distribution can be a list of weights.
           Alternatively, it can be a matrix where each row represents the list of weights for an input value,
           i.e., `probability_distribution[i][j]` is the probability of outputting value j given value i as an input.
        """
        if probability_distribution is None:
            d = DiscreteDistribution.uniform_distribution(num_values)
        else:
            d = probability_distribution

        d_rr = d.with_rr_toss(coin_p)
        return d_rr

    def apply(self, input_value):
        """
        Anonymizes the given input parameter by generalizing it.
        If the input_value is unknown to the distribution and no `default_value` is set, it raises a ValueError.
        """
        try:
            input_idx = self.values.index(input_value)
        except ValueError as e:
            if self.default_value is not None:
                return self.default_value
            raise e
        output_idx = self.cum_distr.sample_element(input_idx)
        return self.values[output_idx]


class RandomizedResponseParameters(CamelBaseModel):
    mechanism: constr(regex="^randomizedResponse$") = "randomizedResponse"
    config: RandomizedResponse
