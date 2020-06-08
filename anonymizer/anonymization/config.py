from typing import Dict, Optional

from ..mechanisms import mechanism_config_types
from ..utils.pydantic_base_model import CamelBaseModel


class AnonymizerConfig(CamelBaseModel):
    default_mechanism: Optional[mechanism_config_types] = None
    mechanisms_by_tag: Dict[str, mechanism_config_types]
