from pydantic import constr

from ._base import MechanismModel


class PseudonymizationParameters(MechanismModel):
    MECHANISM: constr(regex="^pseudonymization$") = "pseudonymization"
    format_string: constr(regex="^[^{}]*{}[^{}]*$")
    initial_counter_value: int = 1

    def build(self):
        return Pseudonymization(self)


class Pseudonymization:
    """
    The pseudonymization mechanisms anonymizes input by replacing it with a formatted string and a counter.
    """

    def __init__(self, format_string, **kwargs):
        """
        Initiates the pseudonymization mechanism.
        This mechanisms takes two parameters: `format_string`, which has to include a replacement field '{}',
        and `initial_counter_value`, which is optional and 1 by default.

        Alternatively, you can pass a `PseudonymizationParameters` object.

        >>> mechanism = Pseudonymization('Person {}')
        >>> mechanism.anonymize('test')
        'Person 1'
        >>> mechanism = Pseudonymization(PseudonymizationParameters(format_string='Person {}'))
        >>> mechanism.anonymize('test')
        'Person 1'
        """
        parameters = (
            format_string
            if isinstance(format_string, PseudonymizationParameters)
            else PseudonymizationParameters(format_string=format_string, **kwargs)
        )
        self.format_string = parameters.format_string
        self.counter = parameters.initial_counter_value

    def anonymize(self, _):
        """
        Anonymizes the given input parameter by pseudonymizing it.
        """
        res = self.format_string.format(self.counter)
        self.counter += 1
        return res
