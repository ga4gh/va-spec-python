"""AMP/ASCO/CAP 2017"""

from ga4gh.va_spec.base.core import (
    Statement,
    VariantDiagnosticProposition,
    VariantPrognosticProposition,
    VariantTherapeuticResponseProposition,
)
from pydantic import (
    Field,
)


class VariantDiagnosticStudyStatement(Statement):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with a disease (a diagnostic inclusion criterion), or absence of a
    disease (diagnostic exclusion criterion) - based on interpretation of the study's
    results.
    """

    proposition: VariantDiagnosticProposition = Field(
        ...,
        description="A proposition about a diagnostic association between a variant and condition, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )


class VariantPrognosticStudyStatement(Statement):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with a disease prognosis - based on interpretation of the study's
    results.
    """

    proposition: VariantPrognosticProposition = Field(
        ...,
        description="A proposition about a prognostic association between a variant and condition, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )


class VariantTherapeuticResponseStudyStatement(Statement):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with a therapeutic response (positive or negative) - based on
    interpretation of the study's results.
    """

    proposition: VariantTherapeuticResponseProposition = Field(
        ...,
        description="A proposition about the therapeutic response associated with a variant, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )
