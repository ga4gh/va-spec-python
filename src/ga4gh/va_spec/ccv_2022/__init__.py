"""Module to load and init namespace at package level."""

from .derived_evidence import (
    CODE_PREFIX_TO_SCORE_MAP,
    CODE_SUFFIX_TO_STRENGTH_MAP,
    derive_onco_evidence_attributes,
)
from .models import (
    VariantOncogenicityEvidenceLine,
    VariantOncogenicityStatement,
)

__all__ = [
    "CODE_PREFIX_TO_SCORE_MAP",
    "CODE_SUFFIX_TO_STRENGTH_MAP",
    "derive_onco_evidence_attributes",
    "VariantOncogenicityEvidenceLine",
    "VariantOncogenicityStatement",
]
