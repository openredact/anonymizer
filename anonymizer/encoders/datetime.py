from datetime import datetime, timezone

from . import Encoder


class DateTimeEncoder(Encoder):
    """
    This encoder can en-/decode date and time strings into float values and back.

    >>> enc = DateTimeEncoder('%I:%M%p')
    >>> enc.decode(enc.encode('10:30AM'))
    '10:30AM'
    >>> enc.encode('10:30AM')
    -2208951000.0
    >>> enc.decode(-2208951000.0 + 60*60)
    '11:30AM'
    """

    def __init__(self, date_format):
        """
        Creates a new DateTimeEncoder based on a given format string.
        """
        self.date_format = date_format

    def encode(self, value):
        dt = datetime.strptime(value, self.date_format).replace(tzinfo=timezone.utc)
        return dt.timestamp()

    def decode(self, value):
        dt = datetime.fromtimestamp(value, tz=timezone.utc)
        return dt.strftime(self.date_format)
