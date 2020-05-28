from pydantic import BaseModel
from typing import Dict, Optional

from ..mechanisms import MechanismModel


class AnonymizerConfig(BaseModel):
    default_mechanism: Optional[MechanismModel]
    mechanisms_by_tag: Dict[str, MechanismModel]
