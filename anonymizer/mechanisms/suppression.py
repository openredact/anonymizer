from typing import Union, Callable

from . import MechanismModel


class SuppressionParameters(MechanismModel):
    suppression_char: str = "X"
    custom_length: Union[int, Callable[[int], int], None] = None

    def build(self):
        return Suppression(parameters=self)


class Suppression:
    """
    The suppression mechanisms anonymizes input by replacing it with a fixed string of the same or custom length.
    """

    def __init__(self, parameters=None, **kwargs):
        """
        Initiates the suppression mechanism.
        This mechanisms takes two, optional parameters: `suppression_char` and `custom_length`.
        Alternatively, the parameters can be passed as a `SuppressionParameters` object via `parameters`.
        >>> mechanism = Suppression(parameters=SuppressionParameters())
        >>> mechanism.anonymize('test')
        'XXXX'

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
        parameters = SuppressionParameters(**kwargs) if parameters is None else parameters
        self.suppression_char = parameters.suppression_char
        self.custom_length = parameters.custom_length

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

    def anonymize(self, input_value):
        """
        Anonymizes the given input parameter by suppressing it.
        """
        output_len = self.__length(len(input_value))
        return self.suppression_char * output_len
