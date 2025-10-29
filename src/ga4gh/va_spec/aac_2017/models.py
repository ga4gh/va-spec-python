"""Profiles defined to align with terminology and conventions from the Association for
Molecular Pathology (AMP), American Society of Clinical Oncology (ASCO), and College of
American Pathologists (CAP) 2017 guidelines for the interpretation and reporting of
sequence variants in cancer.
"""

from abc import ABC
from enum import Enum
from types import MappingProxyType

from pydantic import Field, model_validator
from pydantic.dataclasses import dataclass
from typing_extensions import Self

from ga4gh.core.models import MappableConcept, iriReference
from ga4gh.va_spec.base.core import (
    Direction,
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


class AsmpAscoCapStrengthCode(str, Enum):
    """Define constraints for AMP/ASCO/CAP strength coding"""

    STRONG = "strong"
    POTENTIAL = "potential"


class AmpAscoCapClassificationCode(str, Enum):
    """Define constraints for AMP/ASCO/CAP classification coding"""

    TIER_1 = "tier 1"
    TIER_2 = "tier 2"
    TIER_3 = "tier 3"
    TIER_4 = "tier 4"


AMP_ASCO_CAP_CLASSIFICATION_CODES = [
    v.value for v in AmpAscoCapClassificationCode.__members__.values()
]


class AmpAscoCapClassificationName(str, Enum):
    """Define constraints for AMP/ASCO/CAP classification name"""

    TIER_1 = "Tier I"
    TIER_2 = "Tier II"
    TIER_3 = "Tier III"
    TIER_4 = "Tier IV"


class AmpAscoCapEvidenceLineStrength(str, Enum):
    """Define constraints for AMP/ASCO/CAP `EvidenceLine.strengthOfEvidenceProvided`"""

    A = "A"
    B = "B"
    C = "C"
    D = "D"


AMP_ASCO_CAP_EVIDENCE_LINE_STRENGTHS = [
    v.value for v in AmpAscoCapEvidenceLineStrength.__members__.values()
]


@dataclass
class AmpAscoCapConfig:
    """AMP/ASCO/CAP config for expected values"""

    name: AmpAscoCapClassificationName
    direction: Direction
    strength: AsmpAscoCapStrengthCode | None


AMP_ASCO_CAP_CLASSIFICATION_MAP = MappingProxyType(
    {
        AmpAscoCapClassificationCode.TIER_1: AmpAscoCapConfig(
            name=AmpAscoCapClassificationName.TIER_1,
            direction=Direction.SUPPORTS,
            strength=AsmpAscoCapStrengthCode.STRONG,
        ),
        AmpAscoCapClassificationCode.TIER_2: AmpAscoCapConfig(
            name=AmpAscoCapClassificationName.TIER_2,
            direction=Direction.SUPPORTS,
            strength=AsmpAscoCapStrengthCode.POTENTIAL,
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


class _AmpAscoCapStatement(Statement, ABC):
    """Abstract base class for AAC 2017 statements"""

    @model_validator(mode="after")
    def validate_aac_statement(self) -> Self:
        """Validate AMP/ASCO/CAP statements"""

        def _validate_classification_config(
            classification_code: AmpAscoCapClassificationCode,
            classification_name: str,
            direction: str,
            strength_code: MappableConcept | None,
        ) -> None:
            """Validate that classificati"""
            expected_config = AMP_ASCO_CAP_CLASSIFICATION_MAP[classification_code]
            actual_strength = (
                strength_code.primaryCoding.code.root
                if strength_code
                else strength_code
            )
            if actual_strength != expected_config.strength:
                expected_strength = (
                    expected_config.strength.value
                    if expected_config.strength
                    else expected_config.strength
                )
                msg = f"`strength` must be: {expected_strength}"
                raise ValueError(msg)

            if classification_name != expected_config.name:
                msg = f"`classification.name` must be: {expected_config.name.value}"
                raise ValueError(msg)

            if direction != expected_config.direction:
                msg = f"`direction` must be: {expected_config.direction.value}"
                raise ValueError(msg)

        # Validate strength
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
        _validate_classification_config(
            AmpAscoCapClassificationCode(self.classification.primaryCoding.code.root),
            self.classification.name,
            self.direction,
            self.strength,
        )

        # Validate hasEvidenceLines
        for evidence_line in self.hasEvidenceLines or []:
            if isinstance(evidence_line, EvidenceLine):
                target_proposition = evidence_line.targetProposition
                if target_proposition and not isinstance(
                    target_proposition,
                    VariantDiagnosticProposition
                    | VariantPrognosticProposition
                    | VariantTherapeuticResponseProposition,
                ):
                    msg = "`targetProposition` must be one of: `VariantDiagnosticProposition`, `VariantPrognosticProposition`, `VariantTherapeuticResponseProposition`"
                    raise ValueError(msg)

                validate_mappable_concept(
                    evidence_line.strengthOfEvidenceProvided,
                    System.AMP_ASCO_CAP,
                    valid_codes=AMP_ASCO_CAP_EVIDENCE_LINE_STRENGTHS,
                    mc_is_required=False,
                )

        return self


class VariantDiagnosticStatement(_AmpAscoCapStatement):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with a disease (a diagnostic inclusion criterion), or absence of a
    disease (diagnostic exclusion criterion) - based on interpretation of the study's
    results.
    """

    proposition: VariantClinicalSignificanceProposition = Field(
        ...,
        description="A proposition about a diagnostic association between a variant and condition, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )
    strength: MappableConcept | None = Field(
        default=None,
        description="The strength of support that the Statement is determined to provide for or against the Diagnostic Proposition for the assessed variant, based on the curation and reporting conventions of the AMP/ASCO/CAP (AAC) 2017 Guidelines.",
    )
    classification: MappableConcept = Field(
        ...,
        description="A single term or phrase classifying the subject variant based on the outcome of direction and strength assessments of the Statement's Proposition - reported here using terms from the AMP/ASCO/CAP (AAC) 2017 Guidelines.",
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="A method that specifies how the diagnostic classification was ultimately assigned to the variant, based on assessment of evidence.",
    )


class VariantPrognosticStatement(_AmpAscoCapStatement):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with a disease prognosis - based on interpretation of the study's
    results.
    """

    proposition: VariantClinicalSignificanceProposition = Field(
        ...,
        description="A proposition about a prognostic association between a variant and condition, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )
    strength: MappableConcept | None = Field(
        default=None,
        description="The strength of support that the Statement is determined to provide for or against the Prognostic Proposition for the assessed variant, based on the curation and reporting conventions of the AMP/ASCO/CAP (AAC) 2017 Guidelines.",
    )
    classification: MappableConcept = Field(
        ...,
        description="A single term or phrase classifying the subject variant based on the outcome of direction and strength assessments of the Statement's Proposition - reported here using terms from the AMP/ASCO/CAP (AAC) 2017 Guidelines. Note that the enumerated value set here is bound to the `code` field of the Coding object that is nested inside a MappableConcept's primary coding.",
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="A method that specifies how the prognostic classification was ultimately assigned to the variant, based on assessment of evidence.",
    )


class VariantTherapeuticResponseStatement(_AmpAscoCapStatement):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with a therapeutic response (positive or negative) - based on
    interpretation of the study's results.
    """

    proposition: VariantClinicalSignificanceProposition = Field(
        ...,
        description="A proposition about the therapeutic response associated with a variant, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )
    strength: MappableConcept | None = Field(
        default=None,
        description="The strength of support that the Statement is determined to provide for or against the Therapeutic Response Proposition for the assessed variant, based on the curation and reporting conventions of the AMP/ASCO/CAP (AAC) 2017 Guidelines.",
    )
    classification: MappableConcept = Field(
        ...,
        description="A single term or phrase classifying the subject variant based on the outcome of direction and strength assessments of the Statement's Proposition - reported here using terms from the AMP/ASCO/CAP (AAC) 2017 Guidelines.",
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="A method that specifies how the therapeutic response classification was ultimately assigned to the variant, based on assessment of evidence.",
    )
