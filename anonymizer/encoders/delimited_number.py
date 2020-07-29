import re

from . import Encoder


class DelimitedNumberEncoder(Encoder):
    """
    This encoder can en-/decode numbers with delimiters.
    While the prefix and suffix will be restored upon decoding, the delimiters will be removed.
    Prefix and suffix can contain arbitrary characters. Delimiters are non-word characters only.

    If the number contained exactly one `.` or `,`, it is assumed to be a float.
    Otherwise it is assumed to be an int.

    >>> enc = DelimitedNumberEncoder()
    >>> enc.decode(*enc.encode('12,18 €'))
    '12,18 €'
    >>> v, ctx = enc.encode('12,18 €')
    >>> enc.decode(v + 2.1, ctx)
    '14,28 €'
    """

    delimited_number_regex = re.compile(r"^(\D*?)(-?((\d+)(\W*?))+)(\D*)$")

    def encode(self, value):
        match = DelimitedNumberEncoder.delimited_number_regex.match(value)
        if not match:
            raise ValueError("Invalid input value: does not match pattern for delimited numbers")

        prefix = match.group(1)
        suffix = match.group(6)
        delimited_number = match.group(2)

        # We define a number as float if `.` or `,` occurs exactly once.
        float_delimiter = "." if delimited_number.count(".") == 1 else "," if delimited_number.count(",") == 1 else None

        # Replace float delimiter `,` by `.` if necessary.
        if float_delimiter == ",":
            delimited_number = delimited_number.replace(".", "").replace(",", ".")

        # Remove all delimiters, parse as float.
        sign = "-" if delimited_number.startswith("-") else ""
        number_s = sign + "".join(re.findall(r"[\d.]+", delimited_number))
        precision = len(number_s) - number_s.index(".") - 1 if float_delimiter is not None else 0
        number = float(number_s)

        ctx = dict(prefix=prefix, suffix=suffix, float_delimiter=float_delimiter, precision=precision)

        return number, ctx

    def decode(self, value, ctx):
        try:
            prefix, suffix, float_delimiter, precision = ctx["prefix"], ctx["suffix"], ctx["float_delimiter"], ctx["precision"]
        except (TypeError, KeyError):
            raise ValueError("Invalid context")

        # Post-procession to int if necessary.
        number = f"{value:.{precision}f}"
        if float_delimiter == ",":
            number = number.replace(".", ",")

        return prefix + number + suffix
