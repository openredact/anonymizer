import abc
from typing import Dict

from pydantic import Field

from anonymizer.utils.pydantic_base_model import CamelBaseModel


class StatefulMechanism(CamelBaseModel, abc.ABC):
    """
    The stateful mechanism is a baseclass around any other mechanism.
    If activated, it ensures that several occurrences of the same input
    are anonymized equally (i.e., return the same output).

    >>> from random import randint
    >>> from anonymizer.mechanisms.suppression import Suppression
    >>> mechanism = Suppression(custom_length=lambda _: randint(1, 9), stateful=True)
    >>> assert mechanism.anonymize('foobar') == mechanism.anonymize('foobar')
    """

    stateful: bool = False
    anonymizations: Dict[str, str] = Field(default_factory=dict, const=True)

    @abc.abstractmethod
    def apply(self, input_value):
        """The actual anonymization method of any child class."""

    def anonymize(self, input_value):
        """
        Anonymizes the given input parameter by checking whether it has already been anonymized before.

        If there exists an anonymization, this anonymization is used.
        Otherwise, the inner mechanism is called to provide a new, anonymized output.
        """
        if self.stateful:
            if input_value not in self.anonymizations:
                self.anonymizations[input_value] = self.apply(input_value)
            return self.anonymizations[input_value]
        else:
            return self.apply(input_value)
