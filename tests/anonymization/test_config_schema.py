import pytest
from jsonschema import validate, ValidationError as SchemaValidationError
from pydantic import ValidationError as PydanticValidationError

from anonymizer.anonymization.config import AnonymizerConfig
from anonymizer.mechanisms.suppression import SuppressionParameters
from anonymizer.mechanisms.generalization import GeneralizationParameters


def test_json_schema_is_valid():
    validate(instance={"mechanismsByTag": {"tag1": {"mechanism": "suppression"}}}, schema=AnonymizerConfig.schema())


def test_set_default_from_dict():
    config_dict = {"defaultMechanism": {"mechanism": "suppression"}, "mechanismsByTag": {}}
    validate(instance=config_dict, schema=AnonymizerConfig.schema())
    config = AnonymizerConfig(**config_dict)
    assert type(config.default_mechanism) == SuppressionParameters


def test_pass_custom_length_to_suppression():
    config_dict = {"mechanismsByTag": {"tag1": {"mechanism": "suppression", "customLength": 42}}}
    validate(instance=config_dict, schema=AnonymizerConfig.schema())
    config = AnonymizerConfig(**config_dict)
    assert config.mechanisms_by_tag["tag1"].custom_length == 42


def test_creating_config_wo_passing_mechanism_name():
    config_dict = {"defaultMechanism": {"replacement": "<other>"}, "mechanismsByTag": {"tag1": {"customLength": 42}}}
    validate(instance=config_dict, schema=AnonymizerConfig.schema())
    config = AnonymizerConfig(**config_dict)
    assert type(config.mechanisms_by_tag["tag1"]) == SuppressionParameters
    assert type(config.default_mechanism) == GeneralizationParameters


def test_detect_mismatched_options():
    config_dict = {"mechanismsByTag": {"tag1": {"mechanism": "generalization", "customLength": 42}}}
    with pytest.raises(SchemaValidationError):
        validate(instance=config_dict, schema=AnonymizerConfig.schema())

    with pytest.raises(PydanticValidationError):
        AnonymizerConfig(**config_dict)
