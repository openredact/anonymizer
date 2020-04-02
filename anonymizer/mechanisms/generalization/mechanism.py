class Generalization:
    """
    The generalization mechanisms anonymizes input by replacing it with a more general string.
    It can either be a constant replacement or depend on the input given.
    """

    def __init__(self, replacement):
        """
        Initiates the generalization mechanism.
        This mechanisms takes one parameter: `replacement`.

        The `replacement` parameter defines the how the generalization should be done.
        This parameter can be a constant string or a function that takes the input as a parameter
        and returns the appropriate replacement. Passing a function allows to generate context specific
        replacements.

        >>> mechanism = Generalization('<NAME>')
        >>> mechanism.anonymize('Darth Vader')
        '<NAME>'
        >>> mechanism = Generalization(lambda x: x.split()[0] + ' person')
        >>> mechanism.anonymize('a woman')
        'a person'
        """
        self.replacement = replacement

    def anonymize(self, input_value):
        """
        Anonymizes the given input parameter by generalizing it.
        """
        if callable(self.replacement):
            return self.replacement(input_value)
        else:
            return self.replacement
