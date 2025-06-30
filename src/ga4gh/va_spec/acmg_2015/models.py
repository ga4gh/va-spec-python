"""Profiles defined to align with terminology and conventions from the American College
of Medical Genetics and Genomics (ACMG) 2015 guidelines for interpretation of sequence
variant pathogenicity.
"""

from enum import Enum

from ga4gh.core.models import MappableConcept, iriReference
from ga4gh.va_spec.base.core import (
    EvidenceLine,
    Method,
    Statement,
    VariantPathogenicityProposition,
)
from ga4gh.va_spec.base.enums import (
    CLIN_GEN_CLASSIFICATIONS,
    STRENGTH_OF_EVIDENCE_PROVIDED_VALUES,
    STRENGTHS,
    System,
)
from ga4gh.va_spec.base.validators import (
    validate_mappable_concept,
)
from pydantic import Field, field_validator, model_validator


class AcmgClassification(str, Enum):
    """Define constraints for ACMG classifications"""

    PATHOGENIC = "pathogenic"
    LIKELY_PATHOGENIC = "likely pathogenic"
    BENIGN = "benign"
    LIKELY_BENIGN = "likely benign"
    UNCERTAIN_SIGNIFICANCE = "uncertain significance"


ACMG_CLASSIFICATIONS = [v.value for v in AcmgClassification.__members__.values()]


class VariantPathogenicityEvidenceLine(EvidenceLine):
    """An Evidence Line that describes how a specific type of information was
    interpreted as evidence for or againtst a variant's pathogenicity. In the ACMG
    Framework, evidence is assessed by determining if a specific criterion (e.g. 'PM2')
    with a default strength (e.g. 'moderate') is 'met' or 'not met', and in some cases
    adjusting the default strength based on the quality and abundance of evidence.
    """

    targetProposition: VariantPathogenicityProposition | None = Field(
        None,
        description="A Variant Pathogenicity Proposition against which specific information was assessed, in determining the strength and direction of support this information provides as evidence.",
    )
    strengthOfEvidenceProvided: MappableConcept | None = Field(
        None,
        description="The strength of support that an Evidence Line is determined to provide for or against the proposed pathogenicity of the assessed variant. Strength is evaluated relative to the direction indicated by the 'directionOfEvidenceProvided' attribute. The indicated enumeration constrains the nested MappableConcept.primaryCoding > Coding.code attribute when capturing evidence strength. Conditional requirement: if directionOfEvidenceProvided is either 'supports' or 'disputes', then this attribute is required. If it is 'none', then this attribute is not allowed.",
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="The guidelines that were followed to assess variant information as evidence for or against the assessed variant's pathogenicity.",
    )

    class Criterion(str, Enum):
        """Define ACMG 2015 criterion values"""

        PVS1 = "PVS1"
        PS1 = "PS1"
        PS2 = "PS2"
        PS3 = "PS3"
        PS4 = "PS4"
        PM1 = "PM1"
        PM2 = "PM2"
        PM3 = "PM3"
        PM4 = "PM4"
        PM5 = "PM5"
        PM6 = "PM6"
        PP1 = "PP1"
        PP2 = "PP2"
        PP3 = "PP3"
        PP4 = "PP4"
        PP5 = "PP5"
        BA1 = "BA1"
        BS1 = "BS1"
        BS2 = "BS2"
        BS3 = "BS3"
        BS4 = "BS4"
        BP1 = "BP1"
        BP2 = "BP2"
        BP3 = "BP3"
        BP4 = "BP4"
        BP5 = "BP5"
        BP6 = "BP6"
        BP7 = "BP7"

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
            System.ACMG,
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
        acmg_code_pattern = r"^((?:PVS1)(?:_(?:not_met|(?:strong|moderate|supporting)))?|(?:PS[1-4]|BS[1-4])(?:_(?:not_met|(?:very_strong|moderate|supporting)))?|BA1(?:_not_met)?|(?:PM[1-6])(?:_(?:not_met|(?:very_strong|strong|supporting)))?|(PP[1-5]|BP[1-7])(?:_(?:not_met|very_strong|strong|moderate))?)$"
        return cls._validate_evidence_outcome(values, System.ACMG, acmg_code_pattern)


class VariantPathogenicityStatement(Statement):
    """A Statement describing the role of a variant in causing an inherited condition."""

    proposition: VariantPathogenicityProposition = Field(
        ...,
        description="A proposition about the pathogenicity of a variant, the validity of which is assessed and reported by the Statement. A Statement can put forth the proposition as being true, false, or uncertain, and may provide an assessment of the level of confidence/evidence supporting this claim.",
    )
    strength: MappableConcept | None = Field(
        None,
        description="The strength of support that an ACMG 2015 Variant Pathogenicity statement is determined to provide for or against the proposed pathogenicity of the assessed variant. Strength is evaluated relative to the direction indicated by the 'direction' attribute. The indicated enumeration constrains the nested MappableConcept.primaryCoding > Coding.code attribute when capturing evidence strength.",
    )
    classification: MappableConcept = Field(
        ...,
        description="The classification of the variant's pathogenicity, based on the ACMG 2015 guidelines. These classifications should coincide with the direction and strength values as follows: 'pathogenic' with supports-strong, 'likely pathogenic' with supports-moderate, 'benign' with disputes-strong, 'likely benign' with disputes-moderate 'uncertain significance' can be one of three possibilities... supports-weak, disputes-weak or neutral for uncertain significance (favoring pathogenic), uncertain significance (favoring benign) or uncertain significance (favoring neither pathogenic nor benign). The 'low penetrance' and 'risk allele' versions of pathogenicity classifications would be applied based on whether the variant proposition was defined to have a 'penetrance' of 'low' or 'risk' respectively.",
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="The method that specifies how the pathogenicity classification is ultimately assigned to the variant, based on assessment of evidence.",
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
            v, System.ACMG, valid_codes=STRENGTHS, mc_is_required=False
        )

    @field_validator("classification")
    @classmethod
    def validate_classification(cls, v: MappableConcept) -> MappableConcept:
        """Validate classification

        :param v: classification
        :raises ValueError: If invalid classification values are provided
        :return: Validated classification value
        """
        if not v.primaryCoding:
            err_msg = "`primaryCoding` is required."
            raise ValueError(err_msg)

        supported_systems = [System.ACMG.value, System.CLIN_GEN.value]
        if v.primaryCoding.system not in supported_systems:
            err_msg = f"`primaryCoding.system` must be one of: {supported_systems}."
            raise ValueError(err_msg)

        if v.primaryCoding.system == System.ACMG:
            if v.primaryCoding.code.root not in ACMG_CLASSIFICATIONS:
                err_msg = f"`primaryCoding.code` must be one of {ACMG_CLASSIFICATIONS}."
                raise ValueError(err_msg)
        else:
            if v.primaryCoding.code.root not in CLIN_GEN_CLASSIFICATIONS:
                err_msg = (
                    f"`primaryCoding.code` must be one of {CLIN_GEN_CLASSIFICATIONS}."
                )
                raise ValueError(err_msg)

        return v
