from typing import Union, Callable

from pydantic.types import constr

from .stateful_mechanism import StatefulMechanism
from ..utils.pydantic_base_model import CamelBaseModel


class Suppression(StatefulMechanism):
    """
    The suppression mechanisms anonymizes input by replacing it with a fixed string of the same or custom length.

    This mechanisms takes two, optional parameters: `suppression_char` and `custom_length`.

    The `suppression_char` parameter defines the character to be used for suppression (default: 'X').

    >>> mechanism = Suppression(suppression_char='Y')
    >>> mechanism.anonymize('test')
    'YYYY'

    The `custom_length` parameter defines the length of the suppressed output.
    If the `custom_length` parameter is not set, the length of the input is preserved.
    That means that the input 'foobar' will result in an anonymized output 'XXXXXX'.
    If the `custom_length` parameter is set to 3, the output will be 'XXX' independent of the input.
    To support randomized lengths, this parameter is allowed to be a function that takes
    the input length as a parameter.

    >>> mechanism = Suppression(custom_length=3)
    >>> mechanism.anonymize('foobar')
    'XXX'
    >>> mechanism = Suppression(custom_length=lambda x: x + 1)
    >>> mechanism.anonymize('foobar')
    'XXXXXXX'
    """

    suppression_char: str = "X"
    custom_length: Union[int, Callable[[int], int], None] = None

    class Config:
        @staticmethod
        def schema_extra(schema):
            # manually add the customLength property which is ignored by pydantic because it accepts callables
            schema["properties"]["customLength"] = {"title": "CustomLength", "type": "integer"}

    def __length(self, input_len):
        """
        Determines the length of the suppressed output based on a potentially defined custom length
        and the input length.
        """
        if isinstance(self.custom_length, int) and self.custom_length >= 0:
            return self.custom_length
        elif callable(self.custom_length):
            return self.custom_length(input_len)
        else:
            return input_len

    def apply(self, input_value):
        """
        Anonymizes the given input parameter by suppressing it.
        """
        output_len = self.__length(len(input_value))
        return self.suppression_char * output_len


class SuppressionParameters(CamelBaseModel):
    mechanism: constr(regex="^suppression$") = "suppression"
    config: Suppression
