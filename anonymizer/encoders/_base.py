import abc


class Encoder(abc.ABC):
    """
    An encoder can transform values before they are passed to the anonymization mechanism
    and transforms them back afterwards.

    Note that `decode` should not depend on the original value before anonymization.
    The only exception is purely structural information such as a date format.
    Such information may be passed via the context object.

    A prime example for the usefulness of encoders are dates.
    While human readable forms like "2020-01-02" are common in texts,
    some anonymization techniques require numeric input (e.g., certain forms of Differential Privacy).
    An encoder can transform the date to its UNIX timestamp and transform the anonymized timestamp back to a date.
    """

    @abc.abstractmethod
    def encode(self, value):
        """
        Encodes a value before passing it into a mechanism
        and returns a tuple of this encoding and a context object
        """

    @abc.abstractmethod
    def decode(self, value, ctx):
        """Decodes a value after receiving the result from a mechanism"""

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            title="Encoder", type="object",
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, Encoder):
            raise TypeError("Encoder required")
        return v
