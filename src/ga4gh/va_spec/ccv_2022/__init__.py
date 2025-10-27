"""Module to load and init namespace at package level."""

from .models import (
    VariantOncogenicityEvidenceLine,
    VariantOncogenicityStatement,
)

__all__ = [
    "VariantOncogenicityEvidenceLine",
    "VariantOncogenicityStatement",
]
