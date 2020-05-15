from pydantic import BaseModel, constr


class PseudonymizationParameters(BaseModel):
    format_string: constr(regex="^[^{}]*{}[^{}]*$")
    initial_counter_value: int = 1
