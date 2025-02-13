"""Module to load and init namespace at package level."""

from .models import (
    VariantDiagnosticStudyStatement,
    VariantPrognosticStudyStatement,
    VariantTherapeuticResponseStudyStatement,
)

__all__ = [
    "VariantDiagnosticStudyStatement",
    "VariantPrognosticStudyStatement",
    "VariantTherapeuticResponseStudyStatement",
]
