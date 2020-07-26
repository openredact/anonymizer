import numpy as np
from numpy.random import Generator, PCG64
import pytest

from anonymizer.encoders import EncoderType
from anonymizer.mechanisms.laplace_noise import LaplaceNoise
from anonymizer.utils.dateutil.parser import ParserError


def test_simple():
    mechanism = LaplaceNoise(epsilon=1.0, stateful=True)

    # Temporarily replace rng
    rng = np.random
    np.random = Generator(PCG64(12345))

    assert mechanism.anonymize("0.0") == -0.7881789002823312
    with pytest.raises(ValueError):
        mechanism.anonymize("Foobar")

    np.random = rng


def test_datetime():
    mechanism = LaplaceNoise(epsilon=0.01, stateful=True, encoder=EncoderType.datetime)

    # Temporarily replace rng
    rng = np.random
    np.random = Generator(PCG64(12345))

    assert mechanism.anonymize("2012-01-18") == "2012-01-17"
    with pytest.raises(ParserError):
        mechanism.anonymize("foo")
    assert mechanism.anonymize("2012-01-18") == "2012-01-17"

    assert mechanism.anonymize("2012-01-18 12:21:08") == "2012-01-18 12:20:22"
    assert mechanism.anonymize("12:21:08") == "12:22:38"
    assert mechanism.anonymize("12:21:08") == "12:22:38"

    np.random = rng
