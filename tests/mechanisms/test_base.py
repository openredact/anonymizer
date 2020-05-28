from anonymizer.mechanisms import MechanismModel


def test_abstract():
    # Base model does not result in anything.
    parameters = MechanismModel()
    assert parameters.build() is None
