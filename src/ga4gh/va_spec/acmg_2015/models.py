"""Profiles defined to align with terminology and conventions from the American College
of Medical Genetics and Genomics (ACMG) 2015 guidelines for interpretation of sequence
variant pathogenicity.
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
    VariantPathogenicityProposition,
)
from ga4gh.va_spec.base.enums import (
    CLIN_GEN_CLASSIFICATIONS,
    STRENGTH_CODES,
    STRENGTH_OF_EVIDENCE_PROVIDED_VALUES,
    System,
)
from ga4gh.va_spec.base.validators import (
    _validate_method_type_evidence_outcome,
    validate_mappable_concept,
)

SYSTEM = System.ACMG
METHOD = Method(  # recommended representation of ACMG 2015 method
    name=SYSTEM,
    reportedIn=Document(
        id="pmid:25741868",
        name="Richards et al., 2015, Genet Med.",
        title="Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology",
        doi="10.1038/gim.2015.30",
        pmid="25741868",
        urls=[
            "https://doi.org/10.1038/gim.2015.30",
            "https://pubmed.ncbi.nlm.nih.gov/25741868/",
        ],
    ),
    methodType="guideline",
)


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
    interpreted as evidence for or against a variant's pathogenicity. In the ACMG
    Framework, evidence is assessed by determining if a specific criterion (e.g. 'PM2')
    with a default strength (e.g. 'moderate') is 'met' or 'not met', and in some cases
    adjusting the default strength based on the quality and abundance of evidence.
    """

    targetProposition: VariantPathogenicityProposition | None = Field(
        default=None,
        description="A Variant Pathogenicity Proposition against which a specific type of evidence was assessed, to determine the strength and direction of support this evidence provides for or against the proposition's validity.",
    )
    directionOfEvidenceProvided: Direction = Field(
        ...,
        description="The direction of support that the Evidence Line is determined to provide toward its target Proposition (supports, disputes, neutral). For ACMG-based assessments, if a pathogenicity criterion is 'met' in the Evidence Line the direction is 'supports', if a benignity criterion is 'met' the direction is 'disputes', and if a criteria is 'not met' the direction is 'none'.",
    )
    strengthOfEvidenceProvided: MappableConcept | None = Field(
        default=None,
        description="The strength of support that an Evidence Line is determined to provide for or against the proposed pathogenicity of the assessed variant. Strength is evaluated relative to the direction indicated by the 'directionOfEvidenceProvided' attribute, and captured using a MappableConcept, whose nested 'code' field is bound to an enumerated set of values. Conditional requirement: if `directionOfEvidenceProvided` is either 'supports' or 'disputes', then this attribute is required. If it is 'none', then this attribute is not allowed.",
    )
    specifiedBy: Method | iriReference = Field(
        ...,
        description="The guidelines or rubrics followed in interpreting evidence, to determine the strength and direction of support that it provides for or against a variant's pathogenicity. While the ACMG Criteria themselves provide minimal guidance, typically a more detailed, disease- or gene- specific rubric is followed to determine if a given criterion was met, and how strongly (e.g. the ClinGen Hearing Loss Expert Panel guidelines for ACMG interpretations).",
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

    class MethodType(str, Enum):
        """Define ACMG 2015 method type values"""

        # Assessment of whether population control frequency refutes
        # pathogenicity or whether absence/extreme rarity in controls provides
        # supporting evidence for pathogenicity
        POPULATION_DATA_ASSESSMENT = "Population Data Assessment"

        # Prevalence in affected statistically increased over matched controls,
        # or enrichment in controls inconsistent with disease penetrance
        CASE_CONTROL_ENRICHMENT_ASSESSMENT = "Case-Control Enrichment Assessment"

        # Predicted null variant in a gene where LOF is a known mechanism of disease
        NULL_VARIANT_ASSESSMENT = "Null variant assessment"

        # Same amino acid change as an established pathogenic variant
        SAME_AMINO_ACID_CHANGE_ASSESSMENT = "Same amino acid change assessment"

        # Mutational hot spot or well-established functional domain without
        # benign variation
        MUTATIONAL_HOT_SPOT_AND_FUNCTIONAL_DOMAIN_ASSESSMENT = (
            "Mutational hot spot and functional domain assessment"
        )

        # Protein length change, or in-frame indels changing counts of repeats
        # with no known function
        PROTEIN_LENGTH_CHANGE_ASSESSMENT = "Protein length change assessment"

        # Novel missense change at an amino acid where a different pathogenic
        # missense change has been seen before
        NOVEL_MISSENSE_POSITION_ASSESSMENT = "Novel missense position assessment"

        # Missense in a gene where only truncation causes disease, or with low
        # rate of benign missense variation
        VARIANT_SPECTRUM_ASSESSMENT = "Variant spectrum assessment"

        # Multiple lines of computational evidence support a deleterious effect
        # or no impact
        IN_SILICO_FUNCTIONAL_IMPACT_ASSESSMENT = (
            "In silico functional impact assessment"
        )

        # Silent variant with no predicted splicing impact
        PREDICTED_SILENT_VARIANT_ASSESSMENT = "Predicted silent variant assessment"

        # Well-established functional studies show or do not show deleterious
        # effect
        FUNCTIONAL_DATA_ASSESSMENT = "Functional Data Assessment"

        # Consegregation with disease in multiple family members, or
        # nonsegregation
        SEGREGATION_DATA_ASSESSMENT = "Segregation Data Assessment"

        # De novo, with or without paternity and maternity confirmed
        DE_NOVO_DATA_ASSESSMENT = "De Novo Data Assessment"

        # Observed in trans with a dominant variant, in cis with a pathogenic
        # variant, or in trans with a pathogenic variant in a recessive
        # disorder
        CIS_TRANS_VARIANT_ASSESSMENT = "Cis/trans variant assessment"

        # Benign or pathogenic according to a reputable source
        REPUTABLE_SOURCE_ASSESSMENT = "Reputable Source Assessment"

        # Patient's phenotype or family history highly specific for the gene
        # and disorder
        PHENOTYPE_GENE_SPECIFICITY_ASSESSMENT = "Phenotype-gene specificity assessment"

        # Found in a case with an alternate cause
        ALTERNATIVE_CAUSE_ASSESSMENT = "Alternative cause assessment"

    ALLOWED_CRITERIA_BY_METHOD_TYPE: ClassVar[
        MappingProxyType[
            MethodType,
            frozenset[Criterion],
        ]
    ] = MappingProxyType(
        {
            MethodType.POPULATION_DATA_ASSESSMENT: frozenset(
                {
                    Criterion.BA1,
                    Criterion.BS1,
                    Criterion.PM2,
                }
            ),
            MethodType.CASE_CONTROL_ENRICHMENT_ASSESSMENT: frozenset(
                {
                    Criterion.BS2,
                    Criterion.PM4,
                }
            ),
            MethodType.NULL_VARIANT_ASSESSMENT: frozenset({Criterion.PVS1}),
            MethodType.SAME_AMINO_ACID_CHANGE_ASSESSMENT: frozenset({Criterion.PS1}),
            MethodType.MUTATIONAL_HOT_SPOT_AND_FUNCTIONAL_DOMAIN_ASSESSMENT: frozenset(
                {
                    Criterion.PM1,
                }
            ),
            MethodType.PROTEIN_LENGTH_CHANGE_ASSESSMENT: frozenset(
                {
                    Criterion.PM4,
                    Criterion.BP3,
                }
            ),
            MethodType.NOVEL_MISSENSE_POSITION_ASSESSMENT: frozenset({Criterion.PM5}),
            MethodType.VARIANT_SPECTRUM_ASSESSMENT: frozenset(
                {
                    Criterion.PP2,
                    Criterion.BP1,
                }
            ),
            MethodType.IN_SILICO_FUNCTIONAL_IMPACT_ASSESSMENT: frozenset(
                {
                    Criterion.PP3,
                    Criterion.BP4,
                }
            ),
            MethodType.PREDICTED_SILENT_VARIANT_ASSESSMENT: frozenset({Criterion.BP7}),
            MethodType.FUNCTIONAL_DATA_ASSESSMENT: frozenset(
                {
                    Criterion.PS3,
                    Criterion.BS3,
                }
            ),
            MethodType.SEGREGATION_DATA_ASSESSMENT: frozenset(
                {
                    Criterion.PP1,
                    Criterion.BS4,
                }
            ),
            MethodType.DE_NOVO_DATA_ASSESSMENT: frozenset(
                {
                    Criterion.PS2,
                    Criterion.PM6,
                }
            ),
            MethodType.CIS_TRANS_VARIANT_ASSESSMENT: frozenset(
                {
                    Criterion.PM3,
                    Criterion.BP2,
                }
            ),
            MethodType.REPUTABLE_SOURCE_ASSESSMENT: frozenset(
                {
                    Criterion.PP5,
                    Criterion.BP6,
                }
            ),
            MethodType.PHENOTYPE_GENE_SPECIFICITY_ASSESSMENT: frozenset(
                {
                    Criterion.PP4,
                }
            ),
            MethodType.ALTERNATIVE_CAUSE_ASSESSMENT: frozenset(
                {
                    Criterion.BP5,
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

        :raises ValueError: If ``evidenceOutcome`` exists and is invalid
        :return: Validated input values. If ``evidenceOutcome`` exists.
            Or if ``strengthOfEvidenceProvided`` is not provided when
            ``directionOfEvidenceProvided`` is supports or disputes or if
            ``strengthOfEvidenceProvided`` is provided when
            ``directionOfEvidenceProvided`` is neutral
        """
        self._validate_direction_of_evidence_provided()
        acmg_code_pattern = r"^((?:PVS1)(?:_(?:not_met|(?:strong|moderate|supporting)))?|(?:PS[1-4]|BS[1-4])(?:_(?:not_met|(?:very_strong|moderate|supporting)))?|BA1(?:_not_met)?|(?:PM[1-6])(?:_(?:not_met|(?:very_strong|strong|supporting)))?|(PP[1-5]|BP[1-7])(?:_(?:not_met|very_strong|strong|moderate))?)$"
        self._validate_evidence_outcome(SYSTEM, acmg_code_pattern)
        self._validate_specified_by()
        _validate_method_type_evidence_outcome(
            self.MethodType,
            self.specifiedBy.methodType,
            self.Criterion,
            self.ALLOWED_CRITERIA_BY_METHOD_TYPE,
            self.evidenceOutcome.primaryCoding.code.root,
        )
        return self


class VariantPathogenicityStatement(Statement):
    """A Statement describing the role of a variant in causing an inherited condition."""

    proposition: VariantPathogenicityProposition = Field(
        ...,
        description="A proposition about the pathogenicity of a variant, the validity of which is assessed and reported by the Statement. A Statement can put forth the proposition as being true, false, or uncertain, and may provide an assessment of the level of confidence/evidence supporting this claim.",
    )
    strength: MappableConcept | None = Field(
        default=None,
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
        if not v.primaryCoding:
            err_msg = "`primaryCoding` is required."
            raise ValueError(err_msg)

        supported_systems = [SYSTEM.value, System.CLIN_GEN.value]
        if v.primaryCoding.system not in supported_systems:
            err_msg = f"`primaryCoding.system` must be one of: {supported_systems}."
            raise ValueError(err_msg)

        if v.primaryCoding.system == SYSTEM:
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
