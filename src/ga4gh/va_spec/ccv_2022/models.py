"""Profiles defined to align with terminology and conventions from the Clinical Genome
Resource (ClinGen), Cancer Genomics Consortium (CGC),and Variant Interpretation for
Cancer Consortium (VICC) 2022 community guidelines for cancer variant interpretation.
"""

from enum import Enum

from ga4gh.core.models import MappableConcept, iriReference
from ga4gh.va_spec.base.core import (
    EvidenceLine,
    Method,
    Statement,
    VariantOncogenicityProposition,
)
from ga4gh.va_spec.base.enums import (
    CCV_CLASSIFICATIONS,
    STRENGTH_OF_EVIDENCE_PROVIDED_VALUES,
    STRENGTHS,
    System,
)
from ga4gh.va_spec.base.validators import validate_mappable_concept
from pydantic import Field, field_validator, model_validator


class VariantOncogenicityEvidenceLine(EvidenceLine):
    """An Evidence Line that describes how information about the specific evidence of a
    variant was interpreted as evidence for or against the variant's oncogenicity.
    """

    targetProposition: VariantOncogenicityProposition | None = Field(
        None,
        description="A Variant Oncogenicity Proposition against which evidence information was assessed, in determining the strength and direction of support this information provides as evidence.",
    )
    strengthOfEvidenceProvided: MappableConcept | None = Field(
        None,
        description="The strength of support that an Evidence Line is determined to provide for or against the proposed pathogenicity of the assessed variant. Strength is evaluated relative to the direction indicated by the 'directionOfEvidenceProvided' attribute. The indicated enumeration constrains the nested MappableConcept.primaryCoding > Coding.code attribute when capturing evidence strength.",
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="The guidelines that were followed to assess the variant information as evidence for or against the assessed variant's oncogenicity.",
    )

    class Criterion(str, Enum):
        """Define CCV 2022 criterion values"""

        OVS1 = "OVS1"
        OS1 = "OS1"
        OS2 = "OS2"
        OS3 = "OS3"
        OM1 = "OM1"
        OM2 = "OM2"
        OM3 = "OM3"
        OM4 = "OM4"
        OP1 = "OP1"
        OP2 = "OP2"
        OP3 = "OP3"
        OP4 = "OP4"
        SBVS1 = "SBVS1"
        SBS1 = "SBS1"
        SBS2 = "SBS2"
        SBP1 = "SBP1"
        SBP2 = "SBP2"

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
            v,
            System.CCV,
            valid_codes=STRENGTH_OF_EVIDENCE_PROVIDED_VALUES,
            mc_is_required=False,
        )

    @model_validator(mode="before")
    def validate_model(cls, values: dict) -> dict:  # noqa: N805
        """Validate ``evidenceOutcome`` and ``directionOfEvidenceProvided`` properties

        :param values: Input values
        :raises ValueError: If ``evidenceOutcome`` exists and is invalid
        :return: Validated input values. If ``evidenceOutcome`` exists, then it will be
            validated and converted to a ``MappableConcept``.
            Or if ``strengthOfEvidenceProvided`` is not provided when
            ``directionOfEvidenceProvided`` is supports or disputes or if
            ``strengthOfEvidenceProvided`` is provided when
            ``directionOfEvidenceProvided`` is neutral
        """
        cls._validate_direction_of_evidence_provided(values)
        ccv_code_pattern = r"^((?:OVS1|SBVS1)(?:_(?:not_met|(?:strong|moderate|supporting)))?|(?:OS[1-3]|SBS[1-2])(?:_(?:not_met|(?:very_strong|moderate|supporting)))?|(?:OM[1-4])(?:_(?:not_met|(?:very_strong|strong|supporting)))?|(OP[1-4]|SBP[1-2])(?:_(?:not_met|very_strong|strong|moderate))?)$"
        return cls._validate_evidence_outcome(values, System.CCV, ccv_code_pattern)


class VariantOncogenicityStudyStatement(Statement):
    """A statement reporting a conclusion from a single study about whether a
    variant is associated with oncogenicity (positive or negative) - based on
    interpretation of the study's results.
    """

    proposition: VariantOncogenicityProposition = Field(
        ...,
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
        return validate_mappable_concept(
            v, System.CCV, valid_codes=STRENGTHS, mc_is_required=False
        )

    @field_validator("classification")
    @classmethod
    def validate_classification(cls, v: MappableConcept) -> MappableConcept:
        """Validate classification

        :param v: classification
        :raises ValueError: If invalid classification values are provided
        :return: Validated classification value
        """
        return validate_mappable_concept(
            v, System.CCV, valid_codes=CCV_CLASSIFICATIONS, mc_is_required=True
        )
