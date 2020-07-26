from anonymizer.encoders.datetime import DateTimeEncoder

import pytest


def test_time():
    enc = DateTimeEncoder()

    v, ctx = enc.encode("12:30")
    assert enc.decode(v, ctx) == "12:30"
    assert enc.decode(v + 60 * 60, ctx) == "13:30"
    v, ctx = enc.encode("23:30")
    assert enc.decode(v + 2 * 60 * 60 + 5 * 60, ctx) == "01:35"

    with pytest.raises(ValueError):
        enc.encode("foo")

    with pytest.raises(ValueError):
        enc.decode(123, None)


def test_date():
    enc = DateTimeEncoder()

    v, ctx = enc.encode("11.12.2019")
    assert enc.decode(v, ctx) == "11.12.2019"
    assert enc.decode(v + 60 * 60, ctx) == "11.12.2019"
    v, ctx = enc.encode("31.12.2019")
    assert enc.decode(v + 24 * 60 * 60, ctx) == "01.01.2020"


def test_datetime():
    enc = DateTimeEncoder()

    v, ctx = enc.encode("31.12.2019 12:30")
    assert enc.decode(v, ctx) == "31.12.2019 12:30"
    assert enc.decode(v + 60 * 60, ctx) == "31.12.2019 13:30"
    assert enc.decode(v + 23 * 60 * 60, ctx) == "01.01.2020 11:30"
