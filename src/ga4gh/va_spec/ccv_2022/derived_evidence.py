"""Derive evidence line attributes from a CCV 2022 evidence outcome code.

Can be used to populate `evidenceOutcome`, `directionOfEvidenceProvided`,
`strengthOfEvidenceProvided`, and `scoreOfEvidenceProvided` fields in
`VariantOncogenicityEvidenceLine`.
"""

import re
from types import MappingProxyType
from typing import NamedTuple

from pydantic import BaseModel

from ga4gh.core.models import Coding, MappableConcept, code
from ga4gh.va_spec.base.core import Direction, Method
from ga4gh.va_spec.base.enums import StrengthOfEvidenceProvided, System
from ga4gh.va_spec.ccv_2022.models import (
    CCV_CODE_PATTERN,
    VariantOncogenicityEvidenceLine,
)
from ga4gh.va_spec.ccv_2022.models import (
    METHOD as CCV_METHOD,
)


class EvidenceAttributes(BaseModel):
    """Store the evidence line attributes derived from a CCV outcome code."""

    evidenceOutcome: MappableConcept
    directionOfEvidenceProvided: Direction
    strengthOfEvidenceProvided: MappableConcept | None
    scoreOfEvidenceProvided: int | None
    specifiedBy: Method


class _ParsedEvidenceOutcome(NamedTuple):
    """Store the normalized parts of a CCV evidence outcome code."""

    outcome: str
    criterion: VariantOncogenicityEvidenceLine.Criterion
    modifier: str


# IMPORTANT: Don't change the order. Longer suffixes must be evaluated first.
_CODE_SUFFIX_TO_DEFAULT_STRENGTH_MAP = MappingProxyType(
    {
        "VS": StrengthOfEvidenceProvided.VERY_STRONG,
        "S": StrengthOfEvidenceProvided.STRONG,
        "M": StrengthOfEvidenceProvided.MODERATE,
        "P": StrengthOfEvidenceProvided.SUPPORTING,
    }
)


_STRENGTH_TO_SCORE_MAGNITUDE_MAP = MappingProxyType(
    {
        StrengthOfEvidenceProvided.VERY_STRONG: 8,
        StrengthOfEvidenceProvided.STRONG: 4,
        StrengthOfEvidenceProvided.MODERATE: 2,
        StrengthOfEvidenceProvided.SUPPORTING: 1,
    }
)


def _parse_ccv_evidence_outcome(
    evidence: VariantOncogenicityEvidenceLine.Criterion | str,
) -> _ParsedEvidenceOutcome:
    """Normalize and validate a CCV evidence outcome code.

    :param evidence: A base criterion or complete CCV evidence outcome code.
    :raises ValueError: If the outcome code does not follow the CCV format.
    :return: The canonical outcome code and its parsed parts.
    """
    provided_outcome = (
        evidence.value
        if isinstance(evidence, VariantOncogenicityEvidenceLine.Criterion)
        else evidence
    )
    evidence_code, separator, outcome_modifier = provided_outcome.partition("_")
    outcome_modifier = outcome_modifier.lower()
    evidence_outcome = (
        f"{evidence_code}_{outcome_modifier}" if separator else evidence_code
    )

    if re.fullmatch(CCV_CODE_PATTERN, evidence_outcome) is None:
        msg = f"Invalid CCV evidence outcome: {provided_outcome}"
        raise ValueError(msg)

    criterion = VariantOncogenicityEvidenceLine.Criterion(evidence_code)
    return _ParsedEvidenceOutcome(evidence_outcome, criterion, outcome_modifier)


def derive_onco_evidence_attributes(
    evidence: VariantOncogenicityEvidenceLine.Criterion | str,
) -> EvidenceAttributes:
    """Derive evidence line attributes from a CCV 2022 outcome code.

    :param evidence: A base criterion or complete CCV evidence outcome code.
    :raises ValueError: If the outcome code does not follow the CCV format.
    :return: The attributes needed to populate a CCV evidence line.
    """
    parsed_outcome = _parse_ccv_evidence_outcome(evidence)
    evidence_code = parsed_outcome.criterion.value
    criterion_prefix = evidence_code.rstrip("1234")

    default_strength = next(
        default_strength
        for suffix, default_strength in _CODE_SUFFIX_TO_DEFAULT_STRENGTH_MAP.items()
        if criterion_prefix.endswith(suffix)
    )
    direction, score_sign = (
        (Direction.DISPUTES, -1)
        if evidence_code.startswith("SB")
        else (Direction.SUPPORTS, 1)
    )

    if parsed_outcome.modifier == "not_met":
        applied_strength = None
        direction = Direction.NEUTRAL
    else:
        applied_strength = (
            StrengthOfEvidenceProvided(parsed_outcome.modifier.replace("_", " "))
            if parsed_outcome.modifier
            else default_strength
        )
    system = System.CCV

    return EvidenceAttributes(
        evidenceOutcome=MappableConcept(
            primaryCoding=Coding(code=code(parsed_outcome.outcome), system=system)
        ),
        directionOfEvidenceProvided=direction,
        strengthOfEvidenceProvided=(
            MappableConcept(
                primaryCoding=Coding(code=code(applied_strength), system=system)
            )
            if applied_strength is not None
            else None
        ),
        scoreOfEvidenceProvided=(
            score_sign * _STRENGTH_TO_SCORE_MAGNITUDE_MAP[applied_strength]
            if applied_strength is not None
            else None
        ),
        specifiedBy=CCV_METHOD.model_copy(
            deep=True,
            update={
                "methodType": VariantOncogenicityEvidenceLine.METHOD_TYPE_BY_CRITERION[
                    parsed_outcome.criterion
                ].value
            },
        ),
    )
