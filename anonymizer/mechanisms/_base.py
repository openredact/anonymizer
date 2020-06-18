import abc

from anonymizer.utils.pydantic_base_model import CamelBaseModel


class MechanismModel(CamelBaseModel, abc.ABC):
    @abc.abstractmethod
    def build(self):
        """Builds a mechanism object from the model"""
