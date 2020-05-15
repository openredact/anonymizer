from pydantic import BaseModel
from typing import Union, Callable


class SuppressionParameters(BaseModel):
    suppression_char: str = "X"
    custom_length: Union[int, Callable[[int], int], None] = None
