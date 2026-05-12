"""Profiles defined to align with terminology and conventions from the Clinical Genome
Resource (ClinGen), Cancer Genomics Consortium (CGC),and Variant Interpretation for
Cancer Consortium (VICC) 2022 community guidelines for cancer variant interpretation.
"""

from enum import Enum

from pydantic import Field, field_validator, model_validator

from ga4gh.core.models import MappableConcept, iriReference
from ga4gh.va_spec.base.core import (
    Direction,
    EvidenceLine,
    Method,
    Statement,
    VariantOncogenicityProposition,
)
from ga4gh.va_spec.base.enums import (
    CCV_CLASSIFICATIONS,
    STRENGTH_CODES,
    STRENGTH_OF_EVIDENCE_PROVIDED_VALUES,
    System,
)
from ga4gh.va_spec.base.validators import validate_mappable_concept


class VariantOncogenicityEvidenceLine(EvidenceLine):
    """An Evidence Line that describes how evidence for a variant was interpreted to
    determine if a specific CCV 2022 criterion code is met, and the strength that
    evidence this provides for or against the variant's oncogenicity. An Evidence Line
    that describes how a specific type of information was interpreted as evidence for
    or against a variant's oncogenicity. In the CCV Framework, evidence is assessed by
    determining if a specific criterion (e.g. 'OM2') with a default strength
    (e.g. 'moderate') is 'met' or 'not met', and in some cases adjusting the default
    strength based on the quality and abundance of evidence.
    """

    targetProposition: VariantOncogenicityProposition | None = Field(
        default=None,
        description="A Variant Oncoogenicity Proposition against which a specific type of evidence was assessed, to determine the strength and direction of support this evidence provides for or against the proposition's validity.",
    )
    directionOfEvidenceProvided: Direction = Field(
        ...,
        description="The direction of support that the Evidence Line is determined to provide toward its target Proposition (supports, disputes, neutral). For CCV-based assessments, if a oncogenicity criterion is 'met' in the Evidence Line the direction is 'supports', if a benignity criterion is 'met' the direction is 'disputes', and if a criteria is 'not met' the direction is 'none'.",
    )
    strengthOfEvidenceProvided: MappableConcept | None = Field(
        default=None,
        description="The strength of support that an Evidence Line is determined to provide for or against the proposed oncogenicity of the assessed variant. Strength is evaluated relative to the direction indicated by the 'directionOfEvidenceProvided' attribute, and captured using a MappableConcept, whose nested 'code' field is bound to an enumerated set of values. Conditional requirement: if `directionOfEvidenceProvided` is either 'supports' or 'disputes', then this attribute is required. If it is 'none', then this attribute is not allowed.",
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="The guidelines or rubrics followed in interpreting evidence, to determine the strength and direction of support that it provides for or against a variant's oncogenicity. While the CCV Criteria themselves provide minimal guidance, typically a more detailed, gene- or cancer- specific rubric is followed to determine if a given criterion was met, and how strongly.",
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


class VariantOncogenicityStatement(Statement):
    """A statement reporting a conclusion from a single study about whether a variant is
    associated with oncogenicity (positive or negative) - based on interpretation of the
    study's results.
    """

    proposition: VariantOncogenicityProposition = Field(
        ...,
        description="A proposition about the oncogenicity of a variant, for which the study provides evidence. The validity of this proposition, and the level of confidence/evidence supporting it, may be assessed and reported by the Statement.",
    )
    strength: MappableConcept | None = Field(
        default=None,
        description="The strength of support that an CCV 2022 Oncogenicity statement is determined to provide for or against the proposed oncogenicity of the assessed variant. Strength is evaluated relative to the direction indicated by the 'direction' attribute. The indicated enumeration constrains the nested MappableConcept.primaryCoding > Coding.code attribute when capturing evidence strength. Conditional requirement: if directionOfEvidenceProvided is either 'supports' or 'disputes', then this attribute is required. If it is 'neutral', then this attribute is not allowed.",
    )
    classification: MappableConcept
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
            v, System.CCV, valid_codes=STRENGTH_CODES, mc_is_required=False
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
