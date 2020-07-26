from enum import Enum

from anonymizer.encoders.datetime import DateTimeEncoder


class EncoderType(str, Enum):
    """
    This is used to specify encoders by string values with lazy initialization.
    The main use is for the JSON config.
    """

    datetime = "datetime"

    def to_encoder(self):
        if self == EncoderType.datetime:
            return DateTimeEncoder()
