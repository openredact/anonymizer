import abc
from typing import Optional, Union

from anonymizer.encoders import EncoderType, Encoder
from anonymizer.mechanisms.stateful_mechanism import StatefulMechanism


class EncodingMechanism(StatefulMechanism, abc.ABC):
    """
    The encoding mechanism is a baseclass around other mechanisms that may require encoding.
    It can be used to apply an encoding and decoding step around the actual anonymization.

    >>> from anonymizer.mechanisms.laplace_noise import LaplaceNoise
    >>> from anonymizer.encoders import EncoderType
    >>> import re
    >>> mechanism = LaplaceNoise(epsilon=1, encoder=EncoderType.datetime)
    >>> assert re.fullmatch('\\d{4}-\\d{2}-\\d{2}', mechanism.anonymize('2012-01-18'))
    """

    encoder: Optional[Union[EncoderType, Encoder]] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(self.encoder, EncoderType):
            self.encoder = self.encoder.to_encoder()

    def anonymize(self, input_value):
        """
        Anonymizes the given input parameter and applies en-/decoding.
        """
        if self.encoder:
            value, ctx = self.encoder.encode(input_value)
            anonymized_value = super().anonymize(value)
            return self.encoder.decode(anonymized_value, ctx)
        else:
            return super().anonymize(input_value)
