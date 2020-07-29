from enum import Enum

from anonymizer.encoders.datetime import DateTimeEncoder
from anonymizer.encoders.delimited_number import DelimitedNumberEncoder


class EncoderType(str, Enum):
    """
    This is used to specify encoders by string values with lazy initialization.
    The main use is for the JSON config.
    """

    datetime = "datetime"
    delimited_number = "delimitedNumber"

    def to_encoder(self):
        if self == EncoderType.datetime:
            return DateTimeEncoder()
        elif self == EncoderType.delimited_number:
            return DelimitedNumberEncoder()
