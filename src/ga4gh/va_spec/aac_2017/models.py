"""Profiles defined to align with terminology and conventions from the Association for
Molecular Pathology (AMP), American Society of Clinical Oncology (ASCO), and College of
American Pathologists (CAP) 2017 guidelines for the interpretation and reporting of
sequence variants in cancer.
"""

from enum import Enum
from types import MappingProxyType

from pydantic import Field, RootModel, field_validator, model_validator
from pydantic.dataclasses import dataclass
from typing_extensions import Self

from ga4gh.core.models import BaseModelForbidExtra, MappableConcept, iriReference
from ga4gh.va_spec.base.core import (
    Direction,
    Document,
    EvidenceLine,
    Method,
    Statement,
    VariantClinicalSignificanceProposition,
    VariantDiagnosticProposition,
    VariantPrognosticProposition,
    VariantTherapeuticResponseProposition,
)
from ga4gh.va_spec.base.enums import System
from ga4gh.va_spec.base.validators import validate_mappable_concept

SYSTEM = System.AMP_ASCO_CAP
METHOD = Method(  # recommended representation of AMP/ASCO/CAP 2017 method
    name=SYSTEM,
    reportedIn=Document(
        id="pmid:27993330",
        name="Li et al., 2017, J Mol Diagn.",
        title="Standards and Guidelines for the Interpretation and Reporting of Sequence Variants in Cancer: A Joint Consensus Recommendation of the Association for Molecular Pathology, American Society of Clinical Oncology, and College of American Pathologists",
        doi="10.1016/j.jmoldx.2016.10.002",
        pmid="27993330",
        urls=[
            "https://doi.org/10.1016/j.jmoldx.2016.10.002",
            "https://pubmed.ncbi.nlm.nih.gov/27993330/",
        ],
    ),
    methodType="guideline",
)


class AmpAscoCapEvidenceLineStrength(str, Enum):
    """Define constraints for AMP/ASCO/CAP `EvidenceLine.strengthOfEvidenceProvided`"""

    A = "A"
    B = "B"
    C = "C"
    D = "D"


AMP_ASCO_CAP_EVIDENCE_LINE_STRENGTHS = [
    v.value for v in AmpAscoCapEvidenceLineStrength.__members__.values()
]


class AmpAscoCapEvidenceLine(EvidenceLine):
    """Evidence line for AMP/ASCO/CAP"""

    targetProposition: (
        VariantPrognosticProposition
        | VariantDiagnosticProposition
        | VariantTherapeuticResponseProposition
    )

    @field_validator("strengthOfEvidenceProvided", mode="after")
    @classmethod
    def validate_strength_of_evidence_provided(
        cls, v: MappableConcept | None
    ) -> MappableConcept | None:
        """Validate strengthOfEvidenceProvided"""
        validate_mappable_concept(
            v,
            System.AMP_ASCO_CAP,
            valid_codes=AMP_ASCO_CAP_EVIDENCE_LINE_STRENGTHS,
            mc_is_required=False,
        )
        return v


class _PrognosticEvidenceLineObject(AmpAscoCapEvidenceLine):
    """Internal prognostic evidence line for AMP/ASCO/CAP"""

    targetProposition: VariantPrognosticProposition


class PrognosticEvidenceLine(RootModel[_PrognosticEvidenceLineObject | iriReference]):
    """Prognostic evidence line for AMP/ASCO/CAP"""


class _DiagnosticEvidenceLineObject(AmpAscoCapEvidenceLine):
    """Internal diagnostic evidence line for AMP/ASCO/CAP"""

    targetProposition: VariantDiagnosticProposition


class DiagnosticEvidenceLine(RootModel[_DiagnosticEvidenceLineObject | iriReference]):
    """Diagnostic evidence line for AMP/ASCO/CAP"""


class _TherapeuticEvidenceLineObject(AmpAscoCapEvidenceLine):
    """Internal therapeutic evidence line for AMP/ASCO/CAP"""

    targetProposition: VariantTherapeuticResponseProposition


class TherapeuticEvidenceLine(RootModel[_TherapeuticEvidenceLineObject | iriReference]):
    """Therapeutic evidence line for AMP/ASCO/CAP"""


class AmpAscoCapStrengthCode(str, Enum):
    """Define constraints for AMP/ASCO/CAP strength coding"""

    STRONG = "strong"
    POTENTIAL = "potential"


class AmpAscoCapClassificationCode(str, Enum):
    """Define constraints for AMP/ASCO/CAP classification coding"""

    TIER_1 = "tier i"
    TIER_2 = "tier ii"
    TIER_3 = "tier iii"
    TIER_4 = "tier iv"


AMP_ASCO_CAP_CLASSIFICATION_CODES = [
    v.value for v in AmpAscoCapClassificationCode.__members__.values()
]


class AmpAscoCapClassificationName(str, Enum):
    """Define constraints for AMP/ASCO/CAP classification name"""

    TIER_1 = "Tier I"
    TIER_2 = "Tier II"
    TIER_3 = "Tier III"
    TIER_4 = "Tier IV"


@dataclass
class AmpAscoCapConfig:
    """AMP/ASCO/CAP config for expected values"""

    name: AmpAscoCapClassificationName
    direction: Direction
    strength: AmpAscoCapStrengthCode | None


AMP_ASCO_CAP_CLASSIFICATION_MAP = MappingProxyType(
    {
        AmpAscoCapClassificationCode.TIER_1: AmpAscoCapConfig(
            name=AmpAscoCapClassificationName.TIER_1,
            direction=Direction.SUPPORTS,
            strength=AmpAscoCapStrengthCode.STRONG,
        ),
        AmpAscoCapClassificationCode.TIER_2: AmpAscoCapConfig(
            name=AmpAscoCapClassificationName.TIER_2,
            direction=Direction.SUPPORTS,
            strength=AmpAscoCapStrengthCode.POTENTIAL,
        ),
        AmpAscoCapClassificationCode.TIER_3: AmpAscoCapConfig(
            name=AmpAscoCapClassificationName.TIER_3,
            direction=Direction.NEUTRAL,
            strength=None,
        ),
        AmpAscoCapClassificationCode.TIER_4: AmpAscoCapConfig(
            name=AmpAscoCapClassificationName.TIER_4,
            direction=Direction.DISPUTES,
            strength=None,
        ),
    }
)


class VariantClinicalSignificanceStatement(Statement, BaseModelForbidExtra):
    """A statement reporting a conclusion from a single study about the clinical
    significance of a variant with respect to a condition, based on interpretation of
    the study's results.
    """

    proposition: VariantClinicalSignificanceProposition
    strength: MappableConcept | None = Field(
        default=None,
        description="The strength of support that the Statement is determined to provide for or against the Variant Clinical Significance Proposition for the assessed variant, based on the curation and reporting conventions of the AMP/ASCO/CAP 2017 Guidelines.",
    )
    classification: MappableConcept = Field(
        ...,
        description="A single term or phrase classifying the subject variant based on the outcome of direction and strength assessments of the Statement's Proposition, using terms from the AMP/ASCO/CAP 2017 Guidelines.",
    )
    specifiedBy: Method | iriReference

    @model_validator(mode="after")
    def validate_statement(self) -> Self:
        """Validate VariantClinicalSignificanceStatement"""

        def _validate_evidence_lines(
            classification_code: AmpAscoCapClassificationCode,
            has_evidence_lines: list,
        ) -> None:
            """Validate allowed evidence lines given classification code"""
            approved_el_classes = [
                DiagnosticEvidenceLine,
                PrognosticEvidenceLine,
                TherapeuticEvidenceLine,
            ]
            if classification_code in {
                AmpAscoCapClassificationCode.TIER_1,
                AmpAscoCapClassificationCode.TIER_2,
            }:
                for evidence_line in has_evidence_lines:
                    if hasattr(evidence_line, "root"):
                        el_input = evidence_line.root
                    elif hasattr(evidence_line, "model_dump"):
                        el_input = evidence_line.model_dump()
                    else:
                        el_input = evidence_line

                    for approved_el_cls in approved_el_classes:
                        try:
                            approved_el_cls.model_validate(el_input)
                            break
                        except Exception:  # noqa: S112
                            continue
                    else:
                        msg = "`hasEvidenceLines` must be one of: `DiagnosticEvidenceLine`, `PrognosticEvidenceLine`, or `TherapeuticEvidenceLine`"
                        raise ValueError(msg)

        def _validate_amp_asco_cap_classification_constraints(
            classification_code: AmpAscoCapClassificationCode,
            classification_name: str | None,
            direction: str,
            strength_code: MappableConcept | None,
            has_evidence_lines: list,
        ) -> None:
            """Validate that a classification code enforces required values for
            strength, name, direction, and when applicable allowed evidence line types.
            """
            expected = AMP_ASCO_CAP_CLASSIFICATION_MAP[classification_code]
            actual_strength = (
                strength_code.primaryCoding.code.root
                if strength_code and strength_code.primaryCoding
                else strength_code
            )

            if actual_strength != expected.strength:
                expected_strength = (
                    expected.strength.value if expected.strength else expected.strength
                )
                msg = f"`strength` must be: {expected_strength}"
                raise ValueError(msg)

            if classification_name != expected.name:
                msg = f"`classification.name` must be: {expected.name.value}"
                raise ValueError(msg)

            if direction != expected.direction:
                msg = f"`direction` must be: {expected.direction.value}"
                raise ValueError(msg)

            _validate_evidence_lines(classification_code, has_evidence_lines)

        # Validate strength system. The actual value will be validated in
        # `_validate_amp_asco_cap_classification_constraints`
        validate_mappable_concept(
            self.strength,
            System.AMP_ASCO_CAP,
            mc_is_required=False,
        )

        # Validate classification
        validate_mappable_concept(
            self.classification,
            System.AMP_ASCO_CAP,
            valid_codes=AMP_ASCO_CAP_CLASSIFICATION_CODES,
            mc_is_required=True,
        )

        # Validate values meet AMP/ASCO/CAP classification constraints
        _validate_amp_asco_cap_classification_constraints(
            AmpAscoCapClassificationCode(self.classification.primaryCoding.code.root),
            self.classification.name,
            self.direction,
            self.strength,
            self.hasEvidenceLines or [],
        )

        return self
