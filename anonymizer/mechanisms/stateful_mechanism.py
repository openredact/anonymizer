from . import MechanismModel


class StatefulMechanismParameters(MechanismModel):
    mechanism_config: MechanismModel

    def build(self):
        return StatefulMechanism(self)


class StatefulMechanism:
    """
    A stateful mechanism is a wrapper around any other mechanism.
    It ensures that several occurrences of the same input are anonymized equally (i.e., return the same output).
    """

    def __init__(self, mechanism):
        """
        A stateful mechanism is initialized by providing the inner anonymization mechanism.

        >>> from random import randint
        >>> from anonymizer.mechanisms.suppression import Suppression
        >>> mechanism = StatefulMechanism(Suppression(custom_length=lambda _: randint(1, 9)))
        >>> assert mechanism.anonymize('foobar') == mechanism.anonymize('foobar')

        Alternatively, this can be a `StatefulMechanismParameters` object. In this case,
        initialization will be carried out in the constructor.
        """
        if isinstance(mechanism, StatefulMechanismParameters):
            mechanism = mechanism.mechanism_config.build()

        self.mechanism = mechanism
        self.anonymizations = dict()

    def anonymize(self, input_value):
        """
        Anonymizes the given input parameter by checking whether it has already been anonymized before.

        If there exists an anonymization, this anonymization is used.
        Otherwise, the inner mechanism is called to provide a new, anonymized output.
        """
        if input_value not in self.anonymizations:
            self.anonymizations[input_value] = self.mechanism.anonymize(input_value)
        return self.anonymizations[input_value]
