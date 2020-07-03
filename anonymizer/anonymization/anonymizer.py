from typing import Union, List, Iterator

from anonymizer.anonymization.config import AnonymizerConfig
from anonymizer.anonymization.pii import Pii, AnonymizedPii


class Anonymizer:
    """
    This class provides the higher level API for the anonymizer.
    Given a configuration it can be passed a list or individual `Pii`s
    and returns a list or individual `AnonymizedPii`s.
    """

    def __init__(self, config: AnonymizerConfig):
        """
        Create an Anonymizer from an `AnonymizerConfig`.
        """
        self.default_mechanism = None if config.default_mechanism is None else config.default_mechanism.config
        self.mechanisms_by_tag = {tag: c.config for tag, c in config.mechanisms_by_tag.items()}

    def anonymize(self, piis: Union[Pii, List[Pii]]) -> Union[AnonymizedPii, Iterator[AnonymizedPii]]:
        """
        Anonymizes a list of Piis or an individual Pii.
        """
        if isinstance(piis, Pii):
            return self.anonymize_individual(piis)

        return map(lambda pii: self.anonymize_individual(pii), piis)

    def anonymize_individual(self, pii: Pii) -> AnonymizedPii:
        """
        Anonymizes a single Pii.

        First, it looks up whether there is an anonymization mechanism defined for the Pii's tag.
        If so, it uses that mechanism for anonymization.
        Otherwise, it falls back to the default mechanism.

        If there is no mechanism defined for this tag and the default mechanism is `None`, it is returned unmodified.
        This will be indicated by the `modified` flag of the `AnonymizedPii`.
        """
        # See whether a mechanism is defined.
        if pii.tag in self.mechanisms_by_tag:
            replacement = self.mechanisms_by_tag[pii.tag].anonymize(pii.text)
            return AnonymizedPii.from_pii(pii, replacement)

        # Otherwise try default.
        if self.default_mechanism is not None:
            replacement = self.default_mechanism.anonymize(pii.text)
            return AnonymizedPii.from_pii(pii, replacement)

        return AnonymizedPii.from_pii(pii)
