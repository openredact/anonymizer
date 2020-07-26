import pytest
from pydantic import BaseModel, ValidationError

from anonymizer.encoders import Encoder
from anonymizer.encoders.datetime import DateTimeEncoder


def test_validation():
    class Test(BaseModel):
        foobar: Encoder

    with pytest.raises(ValidationError):
        Test(foobar=1)

    Test(foobar=DateTimeEncoder())
