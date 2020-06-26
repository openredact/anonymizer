from anonymizer.encoders.datetime import DateTimeEncoder

import pytest


def test_time():
    enc = DateTimeEncoder("%H:%M")

    assert enc.decode(enc.encode("12:30")) == "12:30"
    assert enc.decode(enc.encode("12:30") + 60 * 60) == "13:30"
    assert enc.decode(enc.encode("23:30") + 2 * 60 * 60 + 5 * 60) == "01:35"

    with pytest.raises(ValueError):
        enc.encode("foo")


def test_date():
    enc = DateTimeEncoder("%d.%m.%Y")

    assert enc.decode(enc.encode("11.12.2019")) == "11.12.2019"
    assert enc.decode(enc.encode("11.12.2019") + 60 * 60) == "11.12.2019"
    assert enc.decode(enc.encode("31.12.2019") + 24 * 60 * 60) == "01.01.2020"


def test_datetime():
    enc = DateTimeEncoder("%d.%m.%Y %H:%M")

    assert enc.decode(enc.encode("31.12.2019 12:30")) == "31.12.2019 12:30"
    assert enc.decode(enc.encode("31.12.2019 12:30") + 60 * 60) == "31.12.2019 13:30"
    assert enc.decode(enc.encode("31.12.2019 12:30") + 23 * 60 * 60) == "01.01.2020 11:30"
