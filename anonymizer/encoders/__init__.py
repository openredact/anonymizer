import abc


class Encoder(abc.ABC):
    """
    An encoder can transform values before they are passed to the anonymization mechanism
    and transforms them back afterwards.

    Note that `decode` should not depend on the original value before anonymization.

    A prime example for the usefulness of encoders are dates.
    While human readable forms like "2020-01-02" are common in texts,
    some anonymization techniques require numeric input (e.g., certain forms of Differential Privacy).
    An encoder can transform the date to its UNIX timestamp and transform the anonymized timestamp back to a date.
    """

    @abc.abstractmethod
    def encode(self, value):
        """Encodes a value before passing it into a mechanism"""

    @abc.abstractmethod
    def decode(self, value):
        """Decodes a value after receiving the result from a mechanism"""
