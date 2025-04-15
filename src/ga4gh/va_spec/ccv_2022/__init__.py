"""Module to load and init namespace at package level."""

from .models import (
    VariantOncogenicityEvidenceLine,
    VariantOncogenicityStudyStatement,
)

__all__ = [
    "VariantOncogenicityEvidenceLine",
    "VariantOncogenicityStudyStatement",
]
