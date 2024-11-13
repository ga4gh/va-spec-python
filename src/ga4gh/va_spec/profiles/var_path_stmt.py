"""VA Spec Variant Pathogenicity Statement Standard Profile"""

from enum import Enum
from typing import Literal

from ga4gh.cat_vrs.core_models import CategoricalVariant
from ga4gh.core.domain_models import Condition, Gene
from ga4gh.core.entity_models import IRI, Coding, StatementBase
from ga4gh.vrs.models import Variation
from pydantic import ConfigDict, Field


class PenetranceQualifier(str, Enum):
    """Reports the penetrance of the pathogenic effect - i.e. the extent to which the
    variant impact is expressed by individuals carrying it as a measure of the
    proportion of carriers exhibiting the condition.
    """

    HIGH = "high"
    LOW = "low"
    RISK_ALLELE = "risk allele"


class VariantPathogenicityStatement(StatementBase):
    """A Statement describing the role of a variant in causing an inherited condition."""

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["VariantPathogenicityStatement"] = Field(
        "VariantPathogenicityStatement",
        description="MUST be 'VariantPathogenicityStatement'.",
    )
    subjectVariant: Variation | CategoricalVariant | IRI = Field(
        ..., description="A variant that is the subject of the Statement."
    )
    predicate: Literal["isCausalFor"] = Field(
        "isCausalFor",
        description="The relationship declared to hold between the subject and the object of the Statement.",
    )
    objectCondition: Condition | IRI = Field(
        ..., description="The Condition for which the variant impact is stated."
    )
    penetranceQualifier: PenetranceQualifier | None = Field(
        None,
        description="Reports the penetrance of the pathogenic effect - i.e. the extent to which the variant impact is expressed by individuals carrying it as a measure of the proportion of carriers exhibiting the condition.",
    )
    modeOfInheritanceQualifier: list[Coding] | None = Field(
        None,
        description="Reports a pattern of inheritance expected for the pathogenic effect of the variant. Use HPO terms within the hierarchy of 'HP:0000005' (mode of inheritance) to specify.",
    )
    geneContextQualifier: Gene | IRI | None = Field(
        None,
        description="Reports the gene through which the pathogenic effect asserted for the variant is mediated (i.e. it is the variant's impact on this gene that is responsible for causing the condition).",
    )
