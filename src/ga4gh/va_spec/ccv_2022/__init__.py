"""Module to load and init namespace at package level."""

from .derived_evidence import derive_onco_evidence_attributes
from .models import (
    METHOD,
    SYSTEM,
    VariantOncogenicityEvidenceLine,
    VariantOncogenicityStatement,
)

__all__ = [
    "derive_onco_evidence_attributes",
    "METHOD",
    "SYSTEM",
    "VariantOncogenicityEvidenceLine",
    "VariantOncogenicityStatement",
]
