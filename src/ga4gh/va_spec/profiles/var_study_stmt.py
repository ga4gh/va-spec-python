"""VA Spec Variant Study Statement Standard Profiles"""

from enum import Enum
from typing import Literal

from ga4gh.cat_vrs.core_models import CategoricalVariant
from ga4gh.core.domain_models import Condition, Gene, TherapeuticProcedure
from ga4gh.core.entity_models import IRI, StatementBase
from ga4gh.vrs.models import Variation
from pydantic import ConfigDict, Field


class AlleleOriginQualifier(str, Enum):
    """Reports whether the statement should be interpreted in the context of an
    inherited (germline) variant, an acquired (somatic) mutation, or both (combined).
    """

    GERMLINE = "germline"
    SOMATIC = "somatic"
    COMBINED = "combined"


class DiagnosticPredicate(str, Enum):
    """Define constraints for diagnostic predicate"""

    INCLUSIVE = "isDiagnosticInclusionCriterionFor"
    EXCLUSIVE = "isDiagnosticExclusionCriterionFor"


class OncogenicPredicate(str, Enum):
    """Define constraints for oncogenic predicate"""

    ONCOGENIC = "isOncogenicFor"
    PROTECTIVE = "isProtectiveFor"
    PREDISPOSING = "isPredisposingFor"


class PrognosticPredicate(str, Enum):
    """Define constraints for prognostic predicate"""

    BETTER_OUTCOME = "associatedWithBetterOutcomeFor"
    WORSE_OUTCOME = "associatedWithWorseOutcomeFor"


class TherapeuticResponsePredicate(str, Enum):
    """Define constraints for therapeutic response predicate"""

    SENSITIVITY = "predictsSensitivityTo"
    RESISTANCE = "predictsResistanceTo"


class AllelePrevalenceQualifier(str, Enum):
    """Reports whether the statement should be interpreted in the context of the variant
    being rare or common.
    """

    RARE = "rare"
    COMMON = "common"


class VariantDiagnosticStudyStatement(StatementBase):
    """A Statement reporting a conclusion from a single study about whether a variant is
    associated with a disease (a diagnostic inclusion criterion), or absence of a
    disease (diagnostic exclusion criterion) - based on interpretation of the study's
    results.
    """

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["VariantDiagnosticStudyStatement"] = Field(
        "VariantDiagnosticStudyStatement",
        description="MUST be 'VariantDiagnosticStudyStatement'.",
    )
    subjectVariant: Variation | CategoricalVariant | IRI = Field(
        ..., description="A variant that is the subject of the Statement."
    )
    predicate: DiagnosticPredicate = Field(
        ...,
        description="The relationship declared to hold between the subject and the object of the Statement.",
    )
    objectCondition: Condition | IRI = Field(
        ..., description="The disease that is evaluated for diagnosis."
    )
    alleleOriginQualifier: AlleleOriginQualifier | None = Field(
        None,
        description="Reports whether the statement should be interpreted in the context of an inherited (germline) variant, an acquired (somatic) mutation, or both (combined).",
    )
    allelePrevalenceQualifier: AllelePrevalenceQualifier | None = Field(
        None,
        description="Reports whether the statement should be interpreted in the context of the variant being rare or common.",
    )
    geneContextQualifier: Gene | IRI | None = Field(
        None,
        description="Reports a gene impacted by the variant, which may contribute to the diagnostic association  in the Statement.",
    )


class VariantOncogenicityStudyStatement(StatementBase):
    """A Statement reporting a conclusion from a single study that supports or refutes a
    variant's effect on oncogenesis for a specific tumor type - based on interpretation
    of the study's results.
    """

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["VariantOncogenicityStudyStatement"] = Field(
        "VariantOncogenicityStudyStatement",
        description="MUST be 'VariantOncogenicityStudyStatement'.",
    )
    subjectVariant: Variation | CategoricalVariant | IRI = Field(
        ..., description="A variant that is the subject of the Statement."
    )
    predicate: OncogenicPredicate = Field(
        ...,
        description="The relationship declared to hold between the subject and the object of the Statement.",
    )
    objectTumorType: Condition | IRI = Field(
        ..., description="The tumor type for which the variant impact is evaluated."
    )
    alleleOriginQualifier: AlleleOriginQualifier | None = Field(
        None,
        description="Reports whether the statement should be interpreted in the context of an inherited (germline) variant, an acquired (somatic) mutation, or both (combined).",
    )
    allelePrevalenceQualifier: AllelePrevalenceQualifier | None = Field(
        None,
        description="Reports whether the statement should be interpreted in the context of the variant being rare or common.",
    )
    geneContextQualifier: Gene | IRI | None = Field(
        None,
        description="Reports a gene impacted by the variant, which may contribute to the oncogenic role  in the Statement.",
    )


class VariantPrognosticStudyStatement(StatementBase):
    """A Statement reporting a conclusion from a single study about whether a variant is
    associated with an improved or worse outcome for a disease - based on interpretation
    of the study's results.
    """

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["VariantPrognosticStudyStatement"] = Field(
        "VariantPrognosticStudyStatement",
        description="MUST be 'VariantPrognosticStudyStatement'.",
    )
    subjectVariant: Variation | CategoricalVariant | IRI = Field(
        ..., description="A variant that is the subject of the Statement."
    )
    predicate: PrognosticPredicate = Field(
        ...,
        description="The relationship declared to hold between the subject and the object of the Statement.",
    )
    objectCondition: Condition | IRI = Field(
        ..., description="The disease that is evaluated for outcome."
    )
    alleleOriginQualifier: AlleleOriginQualifier | None = Field(
        None,
        description="Reports whether the statement should be interpreted in the context of an inherited (germline) variant, an acquired (somatic) mutation, or both (combined).",
    )
    allelePrevalenceQualifier: AllelePrevalenceQualifier | None = Field(
        None,
        description="Reports whether the statement should be interpreted in the context of the variant being rare or common.",
    )
    geneContextQualifier: Gene | IRI | None = Field(
        None,
        description="Reports a gene impacted by the variant, which may contribute to the prognostic association  in the Statement.",
    )


class VariantTherapeuticResponseStudyStatement(StatementBase):
    """A Statement reporting a conclusion from a single study about the role of a
    variant in modulating the response of a neoplasm to drug administration or other
    therapeutic procedures - based on interpretation of the study's results.
    """

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["VariantTherapeuticResponseStudyStatement"] = Field(
        "VariantTherapeuticResponseStudyStatement",
        description="MUST be 'VariantTherapeuticResponseStudyStatement'.",
    )
    subjectVariant: Variation | CategoricalVariant | IRI = Field(
        ..., description="A variant that is the subject of the Statement."
    )
    predicate: TherapeuticResponsePredicate = Field(
        ...,
        description="The relationship declared to hold between the subject and the object of the Statement.",
    )
    objectTherapeutic: TherapeuticProcedure | IRI = Field(
        ...,
        description="A drug administration or other therapeutic procedure that the neoplasm is intended to respond to.",
    )
    conditionQualifier: Condition | IRI = Field(
        ...,
        description="Reports the disease context in which the variant's association with therapeutic sensitivity or resistance is evaluated. Note that this is a required qualifier in therapeutic response statements.",
    )
    alleleOriginQualifier: AlleleOriginQualifier | None = Field(
        None,
        description="Reports whether the statement should be interpreted in the context of an inherited (germline) variant, an acquired (somatic) mutation, or both (combined).",
    )
    allelePrevalenceQualifier: AllelePrevalenceQualifier | None = Field(
        None,
        description="Reports whether the statement should be interpreted in the context of the variant being rare or common.",
    )
    geneContextQualifier: Gene | IRI | None = Field(
        None,
        description="Reports a gene impacted by the variant, which may contribute to the therapeutic sensitivity or resistance reported in the Statement. ",
    )
