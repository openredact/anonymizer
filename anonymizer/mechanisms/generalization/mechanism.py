from anonymizer.mechanisms.generalization.parameters import GeneralizationParameters


class Generalization:
    """
    The generalization mechanisms anonymizes input by replacing it with a more general string.
    It can either be a constant replacement or depend on the input given.
    """

    def __init__(self, replacement):
        """
        Initiates the generalization mechanism.
        This mechanisms takes one parameter, which defines the how the generalization should be done.

        This parameter can be a constant string or a function that takes the input as a parameter
        and returns the appropriate replacement. Passing a function allows to generate context specific
        replacements.

        Alternatively, the parameter can be a `GeneralizationParameters` object.

        >>> mechanism = Generalization('<NAME>')
        >>> mechanism.anonymize('Darth Vader')
        '<NAME>'
        >>> mechanism = Generalization(lambda x: x.split()[0] + ' person')
        >>> mechanism.anonymize('a woman')
        'a person'
        >>> mechanism = Generalization(GeneralizationParameters(replacement='<NAME>'))
        >>> mechanism.anonymize('Darth Vader')
        '<NAME>'
        """
        parameters = (
            replacement
            if isinstance(replacement, GeneralizationParameters)
            else GeneralizationParameters(replacement=replacement)
        )
        self.replacement = parameters.replacement

    def anonymize(self, input_value):
        """
        Anonymizes the given input parameter by generalizing it.
        """
        if callable(self.replacement):
            return self.replacement(input_value)
        else:
            return self.replacement
