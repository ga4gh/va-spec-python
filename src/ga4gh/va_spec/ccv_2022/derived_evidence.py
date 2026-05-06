"""Provide derived evidence attributes for an onco evidence code.

Can be used to populate `evidenceOutcome`, `strengthOfEvidenceProvided`, and
`scoreOfEvidenceProvided` fields in `VariantOncogenicityEvidenceLine`.
"""

from types import MappingProxyType

from pydantic import BaseModel

from ga4gh.core.models import Coding, MappableConcept, code
from ga4gh.va_spec.base import (
    StrengthOfEvidenceProvided,
)
from ga4gh.va_spec.base.enums import System
from ga4gh.va_spec.ccv_2022.models import VariantOncogenicityEvidenceLine


class EvidenceAttributes(BaseModel):
    """Define derived evidence attributes for an onco evidence code."""

    evidenceOutcome: MappableConcept
    strengthOfEvidenceProvided: MappableConcept
    scoreOfEvidenceProvided: int


# IMPORTANT: Don't change the order. Longer suffixes must be evaluated first.
CODE_SUFFIX_TO_STRENGTH_MAP = MappingProxyType(
    {
        "VS": StrengthOfEvidenceProvided.VERY_STRONG,
        "S": StrengthOfEvidenceProvided.STRONG,
        "M": StrengthOfEvidenceProvided.MODERATE,
        "P": StrengthOfEvidenceProvided.SUPPORTING,
    }
)


CODE_PREFIX_TO_SCORE_MAP = MappingProxyType(
    {
        "OVS": 8,
        "SBVS": -8,
        "OS": 4,
        "SBS": -4,
        "OM": 2,
        "SBM": -2,
        "OP": 1,
        "SBP": -1,
    }
)


def derive_onco_evidence_attributes(
    evidence: VariantOncogenicityEvidenceLine.Criterion,
) -> EvidenceAttributes:
    """Derive evidence attributes given a CCV 2022 evidence code.

    :param evidence: CCV 2022 evidence code
    :return: Derived evidence attributes (evidenceOutcome, strengthOfEvidenceProvided,
        scoreOfEvidenceProvided)
    """
    evidence_code = evidence.value
    normalized_evidence_code = evidence_code.rstrip("1234")

    code_suffix = next(
        suffix
        for suffix in CODE_SUFFIX_TO_STRENGTH_MAP
        if normalized_evidence_code.endswith(suffix)
    )
    code_prefix = next(
        prefix
        for prefix in CODE_PREFIX_TO_SCORE_MAP
        if normalized_evidence_code.startswith(prefix)
    )
    system = System.CCV

    return EvidenceAttributes(
        evidenceOutcome=MappableConcept(
            primaryCoding=Coding(code=code(evidence_code), system=system)
        ),
        strengthOfEvidenceProvided=MappableConcept(
            primaryCoding=Coding(
                code=code(CODE_SUFFIX_TO_STRENGTH_MAP[code_suffix]), system=system
            )
        ),
        scoreOfEvidenceProvided=CODE_PREFIX_TO_SCORE_MAP[code_prefix],
    )
