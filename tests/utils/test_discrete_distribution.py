import random
import pytest

from anonymizer.utils.discrete_distribution import DiscreteDistribution


def test_uniform():
    # Check that a uniform distribution is independent of its input.
    random.seed(0)
    d = DiscreteDistribution.uniform_distribution(10)
    assert len(d) == 10
    c = d.to_cumulative()
    elem1 = c.sample_element(0, rng=random)
    random.seed(0)
    elem2 = c.sample_element(1, rng=random)
    assert elem1 == elem2

    # Check that multiplication on the diagonal by 1 always returns the input value.
    d1 = d.with_rr_toss(1)
    c1 = d1.to_cumulative()
    assert [c1.sample_element(i, rng=random) for i in range(10)] == list(range(10))


def test_simple():
    random.seed(0)
    thrown = False
    try:
        d = DiscreteDistribution([])
    except ValueError:
        thrown = True
    assert thrown

    # Create distribution that always returns 2.
    d = DiscreteDistribution([0, 0, 2, 0, 0])
    c = d.to_cumulative()
    for i in range(20):
        assert c.sample_element(i % 5, rng=random) == 2
    assert len(d) == 5
    assert len(c) == 5

    # Check that multiplication on the diagonal by 1 always returns the input value (simple case).
    weights = []
    for i in range(10):
        weights.append(random.randint(1, 10))
    d = DiscreteDistribution(weights)
    d1 = d.with_rr_toss(1)
    assert len(d1) == 10
    c1 = d1.to_cumulative()
    assert [c1.sample_element(i, rng=random) for i in range(10)] == list(range(10))
    assert len(c1) == 10


def test_matrix():
    random.seed(0)
    # Create distribution that always returns (input + 1) % n.
    weights = []
    for i in range(10):
        weights.append([0] * 10)
        weights[i][(i + 1) % 10] = 1
    d = DiscreteDistribution(weights)
    c = d.to_cumulative()
    for i in range(20):
        assert c.sample_element(i % 10, rng=random) == ((i + 1) % 10)

    # Check that multiplication on the diagonal by 1 always returns the input value (matrix case).
    d1 = d.with_rr_toss(1)
    c1 = d1.to_cumulative()
    assert [c1.sample_element(i, rng=random) for i in range(10)] == list(range(10))


def test_others():
    with pytest.raises(ValueError):
        DiscreteDistribution(0)

    with pytest.raises(ValueError):
        DiscreteDistribution([[[1]]])
