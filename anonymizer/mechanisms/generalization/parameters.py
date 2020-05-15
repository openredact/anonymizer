from pydantic import BaseModel
from typing import Union, Callable


class GeneralizationParameters(BaseModel):
    replacement: Union[str, Callable[[str], str]]
