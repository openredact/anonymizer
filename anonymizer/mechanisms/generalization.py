from typing import Union, Callable

from pydantic.types import constr

from .stateful_mechanism import StatefulMechanism
from ..utils.pydantic_base_model import CamelBaseModel


class Generalization(StatefulMechanism):
    """
    The generalization mechanisms anonymizes input by replacing it with a more general string.
    It can either be a constant replacement or depend on the input given.

    This mechanisms takes one parameter, which defines the how the generalization should be done.

    This parameter can be a constant string or a function that takes the input as a parameter
    and returns the appropriate replacement. Passing a function allows to generate context specific
    replacements.

    >>> mechanism = Generalization(replacement='<NAME>')
    >>> mechanism.anonymize('Darth Vader')
    '<NAME>'
    >>> mechanism = Generalization(replacement=lambda x: x.split()[0] + ' person')
    >>> mechanism.anonymize('a woman')
    'a person'
    """

    replacement: Union[str, Callable[[str], str]]

    class Config:
        @staticmethod
        def schema_extra(schema):
            # manually add the replacement property which is ignored by pydantic because it accepts callables
            schema["properties"]["replacement"] = {"title": "Replacement", "type": "string"}
            schema["required"] = ["replacement"]

    def __anonymize(self, input_value):
        """
        Anonymizes the given input parameter by generalizing it.
        """
        if callable(self.replacement):
            return self.replacement(input_value)
        else:
            return self.replacement


class GeneralizationParameters(CamelBaseModel):
    mechanism: constr(regex="^generalization$") = "generalization"
    config: Generalization
