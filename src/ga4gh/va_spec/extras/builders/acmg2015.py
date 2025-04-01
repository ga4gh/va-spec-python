"""Builders for the ACMG 2015 (v3) guidelines"""

from ga4gh.core.models import Coding, MappableConcept
from ga4gh.va_spec.acmg_2015 import VariantPathogenicityEvidenceLine
from ga4gh.va_spec.base import (
    Direction,
    Document,
    EvidenceLine,
    Method,
    StrengthOfEvidenceProvided,
)

ACMG_2015_SPEC_DOCUMENT = Document(
    name="ACMG 2015 Guidelines",
    pmid=25741868,
    doi="10.1038/gim.2015.30",
    urls=[
        "https://doi.org/10.1038/gim.2015.30",
        "https://www.nature.com/articles/gim201530",
    ],
)


def PS3(  # noqa: N802
    criteria_met: bool = True,
    strength: StrengthOfEvidenceProvided = StrengthOfEvidenceProvided.STRONG,
) -> EvidenceLine:
    """Build an evidence line corresponding to the ACMG 2015 PS3 criterion"""
    code = VariantPathogenicityEvidenceLine.Criterion.PS3.value
    acmg2015_ps3_method = Method(
        name=f"ACMG 2015 {code} Criterion",
        methodType=code,
        reportedIn=ACMG_2015_SPEC_DOCUMENT,
    )

    if not criteria_met:
        strength_mc = None
        direction = Direction.NEUTRAL
        derived_code = f"{code}_not_met"
    else:
        strength_mc = MappableConcept(
            primaryCoding=Coding(code=strength.value, system="ACMG 2015")
        )
        direction = Direction.SUPPORTS
        if strength == StrengthOfEvidenceProvided.STRONG:
            derived_code = code
        else:
            derived_code = f"{code}_{strength.value}"

    return EvidenceLine(
        strengthOfEvidenceProvided=strength_mc,
        directionOfEvidenceProvided=direction,
        specifiedBy=acmg2015_ps3_method,
        evidenceOutcome=MappableConcept(
            primaryCoding=Coding(code=derived_code, system="ACMG 2015")
        ),
    )
