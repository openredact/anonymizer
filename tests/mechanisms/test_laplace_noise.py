import numpy as np
from numpy.random import Generator, PCG64
import pytest

from anonymizer.mechanisms.laplace_noise import LaplaceNoise


def test_simple():
    # Always return true answer.
    mechanism = LaplaceNoise(epsilon=1.0, stateful=True)

    # Temporarily replace rng
    rng = np.random
    np.random = Generator(PCG64(12345))

    assert mechanism.anonymize("0.0") == -0.7881789002823312
    with pytest.raises(ValueError):
        mechanism.anonymize("Foobar")

    np.random = rng
