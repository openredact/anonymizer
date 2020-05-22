from pydantic import BaseModel, validator
from typing import Union, List, Optional

from anonymizer.utils.discrete_distribution import DiscreteDistribution


class RandomizedResponseParameters(BaseModel):
    values: List[str]
    probability_distribution: Union[DiscreteDistribution, List[float], List[List[float]]]
    default_value: Optional[str] = None

    @validator("probability_distribution")
    def distribution_size_matches(cls, v, values, **kwargs):
        if "values" in values:
            num_values = len(values["values"])
            if len(v) != num_values or (
                isinstance(v, list) and any([isinstance(row, list) and len(row) != num_values for row in v])
            ):  # TODO: changes with numpy
                raise ValueError("Size of probability distribution does not match values")
        return v
