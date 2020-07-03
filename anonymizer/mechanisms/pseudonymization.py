from pydantic import constr

from .stateful_mechanism import StatefulMechanism
from ..utils.pydantic_base_model import CamelBaseModel


class Pseudonymization(StatefulMechanism):
    """
    The pseudonymization mechanisms anonymizes input by replacing it with a formatted string and a counter.

    This mechanisms takes two parameters: `format_string`, which has to include a replacement field '{}',
    and `counter`, which provides the optional initial counter value and is `1` by default.

    >>> mechanism = Pseudonymization(format_string='Person {}')
    >>> mechanism.anonymize('test')
    'Person 1'
    """

    format_string: constr(regex="^[^{}]*{}[^{}]*$")
    counter: int = 1

    def __anonymize(self, _):
        """
        Anonymizes the given input parameter by pseudonymizing it.
        """
        res = self.format_string.format(self.counter)
        self.counter += 1
        return res


class PseudonymizationParameters(CamelBaseModel):
    mechanism: constr(regex="^pseudonymization$") = "pseudonymization"
    config: Pseudonymization
