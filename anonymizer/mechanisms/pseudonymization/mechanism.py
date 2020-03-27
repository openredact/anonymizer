class Pseudonymization:
    """
    The pseudonymization mechanisms anonymizes input by replacing it with a formatted string and a counter.
    """

    def __init__(self, format_string, initial_counter_value=1):
        """
        Initiates the pseudonymization mechanism.
        This mechanisms takes two parameters: `format_string`, which has to include a replacement field '{}',
        and `initial_counter_value`, which is optional and 1 by default.

        >>> mechanism = Pseudonymization('Person {}')
        >>> mechanism.anonymize('test')
        'Person 1'
        """
        self.format_string = format_string
        self.counter = initial_counter_value

    def anonymize(self, _):
        """
        Anonymizes the given input parameter by pseudonymizing it.
        """
        res = self.format_string.format(self.counter)
        self.counter += 1
        return res
