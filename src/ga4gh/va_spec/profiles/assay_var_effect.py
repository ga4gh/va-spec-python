"""VA Spec Assay Variant Effect statement and study result Profiles"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from ga4gh.cat_vrs.core_models import CategoricalVariant
from ga4gh.core.entity_models import (
    IRI,
    Coding,
    DataSet,
    Method,
    StatementBase,
    StudyGroup,
    StudyResult,
    StudyResultBase,
)
from ga4gh.vrs.models import MolecularVariation
from pydantic import ConfigDict, Field


class AveFunctionalClassification(str, Enum):
    """The functional classification of the variant effect in the assay."""

    NORMAL = "normal"
    INDETERMINATE = "indeterminate"
    ABNORMAL = "abnormal"


class AveClinicalClassification(str, Enum):
    """The clinical strength of evidence of the variant effect in the assay."""

    PS3_STRONG = "PS3_Strong"
    PS3_MODERATE = "PS3_Moderate"
    PS3_SUPPORTING = "PS3_Supporting"
    BS3_STRONG = "BS3_Strong"
    BS3_MODERATE = "BS3_Moderate"
    BS3_SUPPORTING = "BS3_Supporting"


class AssayVariantEffectFunctionalClassificationStatement(StatementBase):
    """A statement that assigns a functional classification to a variant effect from a functional assay."""

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["AssayVariantEffectFunctionalClassificationStatement"] = Field(
        "AssayVariantEffectFunctionalClassificationStatement",
        description="MUST be 'AssayVariantEffectFunctionalClassificationStatement'.",
    )
    subjectVariant: MolecularVariation | CategoricalVariant | IRI = Field(
        ...,
        description="A protein or genomic contextual or canonical molecular variant.",
    )
    predicate: Literal["hasAssayVariantEffectFor"] = Field(
        "hasAssayVariantEffectFor",
        description="The relationship declared to hold between the subject and the object of the Statement.",
    )
    objectAssay: IRI | Coding = Field(
        ...,
        description="The assay that is evaluated for the variant effect. (e.g growth in haploid cell culture protein stability in fluorescence assay)",
    )
    classification: AveFunctionalClassification = Field(
        ...,
        description="The functional classification of the variant effect in the assay.",
    )
    specifiedBy: Method | IRI | None = Field(
        None,
        description="The method that specifies the functional classification of the variant effect in the assay.",
    )


class AssayVariantEffectClinicalClassificationStatement(StatementBase):
    """A statement that assigns a clinical strength of evidence to a variant effect from a functional assay."""

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["AssayVariantEffectClinicalClassificationStatement"] = Field(
        "AssayVariantEffectClinicalClassificationStatement",
        description="MUST be 'AssayVariantEffectClinicalClassificationStatement'.",
    )
    subjectVariant: MolecularVariation | CategoricalVariant | IRI = Field(
        ...,
        description="A protein or genomic contextual or canonical molecular variant.",
    )
    predicate: Literal["hasAssayVariantEffectFor"] = Field(
        "hasAssayVariantEffectFor",
        description="The relationship declared to hold between the subject and the object of the Statement.",
    )
    objectAssay: IRI | Coding = Field(
        ...,
        description="The assay that is evaluated for the variant effect. (e.g growth in haploid cell culture protein stability in fluorescence assay)",
    )
    classification: AveClinicalClassification = Field(
        ...,
        description="The clinical strength of evidence of the variant effect in the assay.",
    )
    specifiedBy: Method | IRI | None = Field(
        None,
        description="The method that specifies the clinical strength of evidence of the variant effect in the assay.",
    )


class AssayVariantEffectMeasurementStudyResult(StudyResultBase):
    """A StudyResult that reports a variant effect score from a functional assay."""

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["AssayVariantEffectMeasurementStudyResult"] = Field(
        "AssayVariantEffectMeasurementStudyResult",
        description="MUST be 'AssayVariantEffectMeasurementStudyResult'.",
    )
    componentResult: list[StudyResult] | None = Field(
        None,
        description="Another StudyResult comprised of data items about the same focus as its parent Result, but based on a more narrowly scoped analysis of the foundational data (e.g. an analysis based on data about a subset of the parent Results full study population) .",
    )
    studyGroup: StudyGroup | None = Field(
        None,
        description="A description of a specific group or population of subjects interrogated in the ResearchStudy that produced the data captured in the StudyResult.",
    )
    focusVariant: MolecularVariation | IRI | None = Field(
        None,
        description="The human mapped representation of the variant that is the subject of the Statement.",
    )
    score: float | None = Field(
        None, description="The score of the variant effect in the assay."
    )
    specifiedBy: Method | IRI | None = Field(
        None,
        description="The assay that was used to measure the variant effect with all the various properties",
    )
    sourceDataSet: list[DataSet] | None = Field(
        None, description="The full data set that this measurement is a part of"
    )
