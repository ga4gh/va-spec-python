"""Profiles defined to align with terminology and conventions from the Association for
Molecular Pathology (AMP), American Society of Clinical Oncology (ASCO), and College of
American Pathologists (CAP) 2017 guidelines for the interpretation and reporting of
sequence variants in cancer.
"""

from enum import Enum

from ga4gh.core.models import MappableConcept, iriReference
from ga4gh.va_spec.base.core import (
    Method,
    Statement,
    VariantDiagnosticProposition,
    VariantPrognosticProposition,
    VariantTherapeuticResponseProposition,
)
from ga4gh.va_spec.base.enums import System
from pydantic import (
    Field,
    field_validator,
)


class Strength(str, Enum):
    """Define constraints for AMP/ASCO/CAP strength coding"""

    LEVEL_A = "Level A"
    LEVEL_B = "Level B"
    LEVEL_C = "Level C"
    LEVEL_D = "Level D"


AMP_ASCO_CAP_LEVELS = [v.value for v in Strength.__members__.values()]


class Classification(str, Enum):
    """Define constraints for AMP/ASCO/CAP classification coding"""

    TIER_I = "Tier I"
    TIER_II = "Tier II"
    TIER_III = "Tier III"
    TIER_IV = "Tier IV"


AMP_ASCO_CAP_TIERS = [v.value for v in Classification.__members__.values()]


class _ValidatorMixin:
    """Mixin class for reusable AMP/ASCO/CAP field validators"""

    @field_validator("strength")
    @classmethod
    def validate_strength(cls, v: MappableConcept | None) -> MappableConcept | None:
        """Validate strength

        :param v: Strength
        :raises ValueError: If invalid strength values are provided
        :return: Validated strength value
        """
        if not v:
            return v

        if not v.primaryCoding:
            err_msg = "`primaryCoding` is required."
            raise ValueError(err_msg)

        if v.primaryCoding.system != System.AMP_ASCO_CAP:
            err_msg = f"`primaryCoding.system` must be '{System.AMP_ASCO_CAP.value}'."
            raise ValueError(err_msg)

        if v.primaryCoding.code.root not in AMP_ASCO_CAP_LEVELS:
            err_msg = f"`primaryCoding.code` should be one of {AMP_ASCO_CAP_LEVELS}."
            raise ValueError(err_msg)

        return v

    @field_validator("classification")
    @classmethod
    def validate_classification(cls, v: MappableConcept) -> MappableConcept:
        """Validate classification

        :param v: Classification
        :raises ValueError: If invalid classification values are provided
        :return: Validated classification value
        """
        if not v.primaryCoding:
            err_msg = "`primaryCoding` is required."
            raise ValueError(err_msg)

        if v.primaryCoding.system != System.AMP_ASCO_CAP:
            err_msg = f"`primaryCoding.system` must be '{System.AMP_ASCO_CAP.value}'."
            raise ValueError(err_msg)

        if v.primaryCoding.code.root not in AMP_ASCO_CAP_TIERS:
            err_msg = f"`primaryCoding.code` should be one of {AMP_ASCO_CAP_TIERS}."
            raise ValueError(err_msg)

        return v


class VariantDiagnosticStudyStatement(Statement, _ValidatorMixin):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with a disease (a diagnostic inclusion criterion), or absence of a
    disease (diagnostic exclusion criterion) - based on interpretation of the study's
    results.
    """

    proposition: VariantDiagnosticProposition = Field(
        ...,
        description="A proposition about a diagnostic association between a variant and condition, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )
    strength: MappableConcept | None = Field(
        None,
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


class VariantPrognosticStudyStatement(Statement, _ValidatorMixin):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with a disease prognosis - based on interpretation of the study's
    results.
    """

    proposition: VariantPrognosticProposition = Field(
        ...,
        description="A proposition about a prognostic association between a variant and condition, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )
    strength: MappableConcept | None = Field(
        None,
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


class VariantTherapeuticResponseStudyStatement(Statement, _ValidatorMixin):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with a therapeutic response (positive or negative) - based on
    interpretation of the study's results.
    """

    proposition: VariantTherapeuticResponseProposition = Field(
        ...,
        description="A proposition about the therapeutic response associated with a variant, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )
    strength: MappableConcept | None = Field(
        None,
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
