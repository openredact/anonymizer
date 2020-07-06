from typing import Dict, Optional, Union

from ..mechanisms import mechanism_config_types, mechanism_types
from ..utils.pydantic_base_model import CamelBaseModel


class AnonymizerConfig(CamelBaseModel):
    default_mechanism: Optional[Union[mechanism_config_types, mechanism_types]] = None
    mechanisms_by_tag: Dict[str, Union[mechanism_config_types, mechanism_types]]

    class Config:
        @staticmethod
        def schema_extra(schema):
            # Manually cleanup schema: remove all direct instantiations and only allow those ending on `Parameters`
            schema["properties"]["defaultMechanism"]["anyOf"] = [
                v for v in schema["properties"]["defaultMechanism"]["anyOf"] if v["$ref"].endswith("Parameters")
            ]
            schema["properties"]["mechanismsByTag"]["additionalProperties"]["anyOf"] = [
                v
                for v in schema["properties"]["mechanismsByTag"]["additionalProperties"]["anyOf"]
                if v["$ref"].endswith("Parameters")
            ]
