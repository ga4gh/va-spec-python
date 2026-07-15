"""Profiles defined to align with terminology and conventions from the Clinical Genome
Resource (ClinGen), Cancer Genomics Consortium (CGC),and Variant Interpretation for
Cancer Consortium (VICC) 2022 community guidelines for cancer variant interpretation.
"""

from enum import Enum
from types import MappingProxyType
from typing import ClassVar

from pydantic import Field, field_validator, model_validator
from typing_extensions import Self

from ga4gh.core.models import MappableConcept, iriReference
from ga4gh.va_spec.base.core import (
    Direction,
    Document,
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
from ga4gh.va_spec.base.validators import (
    MethodTypeCriterionValidationMixin,
    validate_mappable_concept,
)

SYSTEM = System.CCV
METHOD = Method(  # recommended representation of ClinGen/CGC/VICC 2022 method
    name=SYSTEM,
    reportedIn=Document(
        id="pmid:35101336",
        name="Horak et al., 2022, Genet Med.",
        title="Standards for the classification of pathogenicity of somatic variants in cancer (oncogenicity): Joint recommendations of Clinical Genome Resource (ClinGen), Cancer Genomics Consortium (CGC), and Variant Interpretation for Cancer Consortium (VICC)",
        doi="10.1016/j.gim.2022.01.001",
        pmid="35101336",
        urls=[
            "https://doi.org/10.1016/j.gim.2022.01.001",
            "https://pubmed.ncbi.nlm.nih.gov/35101336/",
        ],
    ),
    methodType="guideline",
)


class VariantOncogenicityEvidenceLine(EvidenceLine, MethodTypeCriterionValidationMixin):
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

    class MethodType(str, Enum):
        """Define CCV 2022 method type values"""

        # Assessment of whether population control frequency refutes
        # oncogenicity or whether absence/extreme rarity in controls provides
        # supporting evidence for oncogenicity
        POPULATION_FREQUENCY = "population_frequency"

        # Assessment of well-established in vitro or in vivo functional studies
        # to determine whether experimental evidence supports or refutes an
        # oncogenic effect
        FUNCTIONAL_ASSAY = "functional_assay"

        # Assessment of the primary sequence-level consequence of the variant,
        # including null/loss-of-function effects, protein-length changes,
        # stop-loss effects, or synonymous variants predicted to have no
        # splice or conservation impact
        PRIMARY_SEQUENCE_CONSEQUENCE = "primary_sequence_consequence"

        # Assessment of whether the variant occurs in a critical and
        # well-established functional domain or region, such as an enzyme
        # active site
        FUNCTIONAL_DOMAIN_LOCATION = "functional_domain_location"

        # Assessment by analogy to previously established oncogenic variants,
        # including the same amino acid change or a different missense change
        # at the same residue
        AMINO_ACID_OR_RESIDUE_ANALOGY = "amino_acid_or_residue_analogy"

        # Assessment of somatic recurrence at cancer hotspots or recurrently
        # mutated residues, with evidence strength based on recurrence
        # thresholds
        SOMATIC_HOTSPOT_RECURRENCE = "somatic_hotspot_recurrence"

        # Aggregate assessment of computational predictions, including
        # conservation, missense-effect, and splice-effect tools, supporting
        # either oncogenic effect or no effect
        COMPUTATIONAL_PREDICTION = "computational_prediction"

        # Assessment of whether the variant occurs in a gene and malignancy
        # context where the disease has a single genetic etiology, making that
        # gene-level event supportive of oncogenicity
        SINGLE_GENETIC_ETIOLOGY_CONTEXT = "single_genetic_etiology_context"

    ALLOWED_CRITERIA_BY_METHOD_TYPE: ClassVar[
        MappingProxyType[MethodType, frozenset[Criterion]]
    ] = MappingProxyType(
        {
            MethodType.POPULATION_FREQUENCY: frozenset(
                {
                    Criterion.SBVS1,
                    Criterion.SBS1,
                    Criterion.OP4,
                }
            ),
            MethodType.FUNCTIONAL_ASSAY: frozenset(
                {
                    Criterion.OS2,
                    Criterion.SBS2,
                }
            ),
            MethodType.PRIMARY_SEQUENCE_CONSEQUENCE: frozenset(
                {
                    Criterion.OVS1,
                    Criterion.OM2,
                    Criterion.SBP2,
                }
            ),
            MethodType.FUNCTIONAL_DOMAIN_LOCATION: frozenset(
                {
                    Criterion.OM1,
                }
            ),
            MethodType.AMINO_ACID_OR_RESIDUE_ANALOGY: frozenset(
                {
                    Criterion.OS1,
                    Criterion.OM4,
                }
            ),
            MethodType.SOMATIC_HOTSPOT_RECURRENCE: frozenset(
                {
                    Criterion.OS3,
                    Criterion.OM3,
                    Criterion.OP3,
                }
            ),
            MethodType.COMPUTATIONAL_PREDICTION: frozenset(
                {
                    Criterion.OP1,
                    Criterion.SBP1,
                }
            ),
            MethodType.SINGLE_GENETIC_ETIOLOGY_CONTEXT: frozenset(
                {
                    Criterion.OP2,
                }
            ),
        }
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
            v,
            SYSTEM,
            valid_codes=STRENGTH_OF_EVIDENCE_PROVIDED_VALUES,
            mc_is_required=False,
        )

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        """Validate ``evidenceOutcome`` and ``directionOfEvidenceProvided`` properties

        :raises ValueError: If ``evidenceOutcome`` exists and is invalid.
            Or if ``strengthOfEvidenceProvided`` is not provided when
            ``directionOfEvidenceProvided`` is supports or disputes or if
            ``strengthOfEvidenceProvided`` is provided when
            ``directionOfEvidenceProvided`` is neutral
        """
        self._validate_direction_of_evidence_provided()
        ccv_code_pattern = r"^((?:OVS1|SBVS1)(?:_(?:not_met|(?:strong|moderate|supporting)))?|(?:OS[1-3]|SBS[1-2])(?:_(?:not_met|(?:very_strong|moderate|supporting)))?|(?:OM[1-4])(?:_(?:not_met|(?:very_strong|strong|supporting)))?|(OP[1-4]|SBP[1-2])(?:_(?:not_met|very_strong|strong|moderate))?)$"
        self._validate_evidence_outcome(SYSTEM, ccv_code_pattern, is_required=True)
        self._validate_specified_by()
        self._validate_method_type_evidence_outcome(
            self.specifiedBy.methodType, self.evidenceOutcome.primaryCoding.code.root
        )
        return self


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
            v, SYSTEM, valid_codes=STRENGTH_CODES, mc_is_required=False
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
            v, SYSTEM, valid_codes=CCV_CLASSIFICATIONS, mc_is_required=True
        )
