"""Profiles defined to align with terminology and conventions from the Clinical Genome
Resource (ClinGen), Cancer Genomics Consortium (CGC),and Variant Interpretation for
Cancer Consortium (VICC) 2022 community guidelines for cancer variant interpretation.
"""

from enum import Enum

from ga4gh.core.models import MappableConcept, iriReference
from ga4gh.va_spec.base.core import (
    EvidenceLineValidatorMixin,
    Method,
    StatementValidatorMixin,
    VariantOncogenicityProposition,
)
from ga4gh.va_spec.base.enums import (
    CCV_CLASSIFICATIONS,
    STRENGTH_OF_EVIDENCE_PROVIDED_VALUES,
    STRENGTHS,
    System,
)
from ga4gh.va_spec.base.validators import validate_mappable_concept
from pydantic import BaseModel, Field, field_validator, model_validator


class EvidenceOutcome(str, Enum):
    """Define constraints for evidence outcome values"""

    OS2 = "OS2"
    OS2_MODERATE = "OS2_moderate"
    OS2_SUPPORTING = "OS2_supporting"
    OS2_NOT_MET = "OS2_not_met"
    SBS2 = "SBS2"
    SBS2_MODERATE = "SBS2_moderate"
    SBS2_SUPPORTING = "SBS2_supporting"
    SBS2_NOT_MET = "SBS2_not_met"


EVIDENCE_OUTCOME_VALUES = [v.value for v in EvidenceOutcome.__members__.values()]


class VariantOncogenicityFunctionalImpactEvidenceLine(
    BaseModel, EvidenceLineValidatorMixin
):
    """An Evidence Line that describes how information about the functional impact of a
    variant on a gene or gene product was interpreted as evidence for or against the
    variant's oncogenicity.
    """

    targetProposition: VariantOncogenicityProposition | None = Field(
        None,
        description="A Variant Oncogenicity Proposition against which functional impact information was assessed, in determining the strength and direction of support this information provides as evidence.",
    )
    strengthOfEvidenceProvided: MappableConcept | None = Field(
        None,
        description="The strength of support that an Evidence Line is determined to provide for or against the proposed pathogenicity of the assessed variant. Strength is evaluated relative to the direction indicated by the 'directionOfEvidenceProvided' attribute. The indicated enumeration constrains the nested MappableConcept.primaryCoding > Coding.code attribute when capturing evidence strength.",
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="The Clingen/CGC/VICC 2022 criterion that was applied to interpret variant functional impact information as evidence for or against the assessed variant's oncogenicity.",
    )

    @field_validator("strengthOfEvidenceProvided")
    @classmethod
    def validate_strength_of_evidence_provided(
        cls, v: MappableConcept | None
    ) -> MappableConcept | None:
        """Validate strengthOfEvidenceProvided

        :param v: strengthOfEvidenceProvided
        :raises ValueError: If invalid strengthOfEvidenceProvided values are provided
        :return: Validated strengthOfEvidenceProvided value
        """
        return validate_mappable_concept(
            v, System.CCV, STRENGTH_OF_EVIDENCE_PROVIDED_VALUES, mc_is_required=False
        )

    @model_validator(mode="before")
    def validate_evidence_outcome(cls, values: dict) -> dict:  # noqa: N805
        """Validate ``evidenceOutcome`` property if it exists

        :param values: Input values
        :raises ValueError: If ``evidenceOutcome`` exists and is invalid
        :return: Validated input values. If ``evidenceOutcome`` exists, then it will be
            validated and converted to a ``MappableConcept``
        """
        return cls._validate_evidence_outcome(
            values, System.CCV, EVIDENCE_OUTCOME_VALUES
        )


class VariantOncogenicityStudyStatement(BaseModel, StatementValidatorMixin):
    """A statement reporting a conclusion from a single study about whether a
    variant is associated with oncogenicity (positive or negative) - based on
    interpretation of the study's results.
    """

    proposition: VariantOncogenicityProposition | None = Field(
        None,
        description="A proposition about the oncogenicity of a variant, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )
    strength: MappableConcept | None = Field(
        None,
        description="The strength of support that an CCV 2022 Oncogenicity statement is determined to provide for or against the proposed oncogenicity of the assessed variant. Strength is evaluated relative to the direction indicated by the 'direction' attribute. The indicated enumeration constrains the nested MappableConcept.primaryCoding > Coding.code attribute when capturing evidence strength.",
    )
    classification: MappableConcept = Field(
        ...,
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="The method that specifies how the oncogenicity classification is ultimately assigned to the variant, based on assessment of evidence.",
    )

    @field_validator("strength")
    @classmethod
    def validate_strength(cls, v: MappableConcept | None) -> MappableConcept | None:
        """Validate strength

        :param v: strength
        :raises ValueError: If invalid strength values are provided
        :return: Validated strength value
        """
        return validate_mappable_concept(v, System.CCV, STRENGTHS, mc_is_required=False)

    @field_validator("classification")
    @classmethod
    def validate_classification(cls, v: MappableConcept) -> MappableConcept:
        """Validate classification

        :param v: classification
        :raises ValueError: If invalid classification values are provided
        :return: Validated classification value
        """
        return validate_mappable_concept(
            v, System.CCV, CCV_CLASSIFICATIONS, mc_is_required=True
        )
