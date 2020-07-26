from datetime import datetime
from anonymizer.utils.dateutil.parser import parse

from . import Encoder


class DateTimeEncoder(Encoder):
    """
    This encoder can en-/decode date and time strings into float values and back.
    The encoder will automatically detect the input format and return it via the context object.

    >>> enc = DateTimeEncoder()
    >>> enc.decode(*enc.encode('10:30AM'))
    '10:30AM'
    >>> v, ctx = enc.encode('10:30AM')
    >>> enc.decode(v + 60*60, ctx)
    '11:30AM'
    """

    def encode(self, value):
        dt, fmt = parse(value, return_format=True)
        ctx = dict(fmt=fmt, tz=dt.tzinfo)
        return dt.timestamp(), ctx

    def decode(self, value, ctx):
        try:
            tz, fmt = ctx["tz"], ctx["fmt"]
        except (TypeError, KeyError):
            raise ValueError("Invalid context")

        dt = datetime.fromtimestamp(value, tz=tz)
        return dt.strftime(fmt)
