"""
The Pii class is the interface to other components of OpenRedact.
"""

from dataclasses import dataclass


@dataclass
class Pii:
    tag: str
    text: str
    id: int = None  # An optional identifier for the entity to be anonymized.


@dataclass
class AnonymizedPii(Pii):
    modified: bool = False

    @staticmethod
    def from_pii(pii: Pii, replacement: str = None):
        """
        Creates the equivalent `AnonymizedPii` for a given Pii.
        """
        return AnonymizedPii(
            tag=pii.tag, text=pii.text if replacement is None else replacement, id=pii.id, modified=replacement is not None
        )
