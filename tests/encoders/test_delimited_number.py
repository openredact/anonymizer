import pytest

from anonymizer.encoders.delimited_number import DelimitedNumberEncoder


def test_phone():
    enc = DelimitedNumberEncoder()

    v, ctx = enc.encode("+49 123 456-789")
    assert enc.decode(v, ctx) == "+49123456789"
    assert enc.decode(v + 1, ctx) == "+49123456790"

    v, ctx = enc.encode("+1 (203) 11-111")
    assert enc.decode(v, ctx) == "+120311111"

    v, ctx = enc.encode("+1 (203) 11-111 CALL ME")
    assert enc.decode(v, ctx) == "+120311111 CALL ME"

    with pytest.raises(ValueError):
        enc.encode("foo")

    with pytest.raises(ValueError):
        enc.encode("+1 (203) CALL ME 521")

    with pytest.raises(ValueError):
        enc.decode(123, None)


def test_unit():
    enc = DelimitedNumberEncoder()

    v, ctx = enc.encode("12.14$")
    assert enc.decode(v, ctx) == "12.14$"
    assert enc.decode(v + 2.1, ctx) == "14.24$"
    assert enc.decode(v + 2.103, ctx) == "14.24$"
    assert enc.decode(v + 2.159, ctx) == "14.30$"

    v, ctx = enc.encode("EURO 12,14")
    assert enc.decode(v, ctx) == "EURO 12,14"
    assert enc.decode(v + 2.1, ctx) == "EURO 14,24"

    v, ctx = enc.encode("EURO -12,14")
    assert enc.decode(v, ctx) == "EURO -12,14"
    assert enc.decode(v + 24, ctx) == "EURO 11,86"

    v, ctx = enc.encode("100,000,000€")
    assert enc.decode(v, ctx) == "100000000€"

    v, ctx = enc.encode("100,000,000.12€")
    assert enc.decode(v, ctx) == "100000000.12€"

    v, ctx = enc.encode("100.000.000,12€")
    assert enc.decode(v, ctx) == "100000000,12€"
