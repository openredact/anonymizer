from typing import Dict, Optional

from ..mechanisms import MechanismModel
from ..utils.pydantic_base_model import CamelBaseModel


class AnonymizerConfig(CamelBaseModel):
    default_mechanism: Optional[MechanismModel]
    mechanisms_by_tag: Dict[str, MechanismModel]
