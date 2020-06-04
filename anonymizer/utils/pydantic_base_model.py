from pydantic import BaseModel


def to_camel_case(snake_case):
    pascal_case = snake_case.title().replace("_", "")
    return pascal_case[0].lower() + pascal_case[1:]


class CamelBaseModel(BaseModel):
    """This base model automatically adds camelCase aliases."""

    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True
