import random

import numpy as np


class DiscreteDistribution:
    """
    This class represents a (conditional) discrete probability distribution.
    More specifically, it stores the probabilities `P(output = j | input = i)`
    of generating an output j given an input i.
    Generally, such a distribution is represented by a matrix where p_ij denotes
    the entry in row i and column j.

    Each row is guaranteed to sum up to 1 to satisfy the property of a probability distribution.

    As an optimization, if `P(output = j | input = i) = P(output = j)`, i.e., the distribution is independent
    of the input value, only a single row is stored.
    """

    def __init__(self, weights):
        """
        Creates a new discrete distribution.
        The input can be either a list of weights (if `P(output = j | input = i) = P(output = j)`),
        or a matrix of weights.

        This method will take care of normalizing the weights, so that each row sums up to 1.
        """
        if not isinstance(weights, np.ndarray):
            weights = np.array(weights)

        if weights.dtype == np.dtype("O"):
            raise ValueError("Weights must be a list or matrix of number types")
        if len(weights.shape) not in (1, 2):
            raise ValueError("Weights must be a list or matrix")
        if any([length < 1 for length in weights.shape]):
            raise ValueError("Cannot create an empty probability distribution")

        self.probabilities = weights
        self.is_matrix = len(weights.shape) == 2
        self.normalize()

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            title="DiscreteDistribution",
            type="object",
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, DiscreteDistribution):
            raise TypeError("DiscreteDistribution required")
        return v

    @classmethod
    def uniform_distribution(cls, n):
        """
        Creates a uniform distribution over n values.
        """
        return UniformDistribution(n)

    def normalize(self):
        """
        Normalizes the weights to ensure that each row sums up to 1.

        This is achieved by dividing each entry by the sum of all probabilities.
        If the weights are a matrix, the operation is performed per row.
        """
        if self.is_matrix:
            # Matrix case
            norm = np.abs(self.probabilities).sum(axis=1)[np.newaxis]
            self.probabilities = self.probabilities / norm.transpose()
        else:
            # Array case
            norm = np.abs(self.probabilities).sum()
            self.probabilities = self.probabilities / norm

    def to_full_distribution(self):
        """
        Returns the full matrix representation for any discrete distribution representation.
        This allows to have a consistent representation for operations on the matrix.

        If the current distribution is already represented as a matrix, self is returned.
        """
        if self.is_matrix:
            return self
        else:
            size = self.probabilities.shape[0]
            probabilities = np.tile(self.probabilities, (size, size))
            return DiscreteDistribution(probabilities)

    def to_cumulative(self):
        """
        Returns the corresponding cumulative distribution.
        The cumulative distribution is used for sampling.
        """
        return CumulativeDiscreteDistribution(self)

    def with_rr_toss(self, p):
        """
        Simulates a randomized response toss with a probability of p for reporting the true value.
        This results in a probability of p'_ii = p + (1 - p) * p_ii along the diagonal
        and multiplies all other probabilities by (1 - p).

        Returns a new distribution and does not modify the current one.
        """
        full = self.to_full_distribution()
        # Multiply each entry by (1 - p)
        full.probabilities *= 1 - p

        # Create diagonal matrix with p
        diag = np.zeros(full.probabilities.shape)
        np.fill_diagonal(diag, p)

        # Add p along diagonal
        full.probabilities += diag
        return full

    def __len__(self):
        """
        Returns the number of items in the distribution.
        """
        return len(self.probabilities)


class CumulativeDiscreteDistribution:
    """
    A cumulative representation of a discrete probability distribution.
    This can be used to speed up sampling.
    """

    def __init__(self, discrete_distribution):
        """
        Creates a new cumulative distribution from a DiscreteDistribution.
        """
        if discrete_distribution.is_matrix:
            self.cum_probabilities = np.cumsum(discrete_distribution.probabilities, axis=1)
            self.is_matrix = True
        else:
            self.cum_probabilities = np.cumsum(discrete_distribution.probabilities)
            self.is_matrix = False

    def sample_element(self, input_idx, rng=random.SystemRandom()):
        """
        Samples an output index j based in the given input index `input_idx`
        according to the distribution `P(output = j | input = i)`.

        Optionally takes an random number generator that implements the method `choices` following `random.choices`.
        By default, SystemRandom is used.
        """
        row = self.cum_probabilities
        if self.is_matrix:
            row = self.cum_probabilities[input_idx]
        return rng.choices(range(len(row)), cum_weights=row)[0]

    def __len__(self):
        """
        Returns the number of items in the distribution.
        """
        return len(self.cum_probabilities)


class UniformDistribution(DiscreteDistribution, CumulativeDiscreteDistribution):
    """
    The uniform distribution is a special case of a distribution, which can efficiently be represented by
    the number of possible values n (also for the cumulative distribution).
    """

    def __init__(self, n):
        """
        Instantiates a uniform distribution over n values.
        """
        super().__init__([1])
        self.n = n

    def normalize(self):
        """
        No need for normalization here.
        """
        pass

    def to_full_distribution(self):
        """
        Returns the full matrix representation for any discrete distribution representation.
        This allows to have a consistent representation for operations on the matrix.
        """
        probabilities = np.ones((self.n, self.n))
        return DiscreteDistribution(probabilities)

    def to_cumulative(self):
        """
        Returns the corresponding cumulative distribution.
        The cumulative distribution is used for sampling.
        """
        return self

    def sample_element(self, input_idx, rng=random.SystemRandom()):
        """
        Samples an output index j based in the given input index `input_idx`
        according to the distribution `P(output = j | input = i)`.

        Optionally takes an random number generator that implements the method `choices` following `random.choices`.
        By default, SystemRandom is used.
        """
        return rng.choices(range(self.n))[0]

    def __len__(self):
        """
        Returns the number of items in the distribution.
        """
        return self.n
