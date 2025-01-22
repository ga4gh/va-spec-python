"""Cohort Allele Frequency Study Result Standard Profile"""

from typing import Literal

from ga4gh.core.models import iriReference
from ga4gh.va_spec.base.core import StudyResultBase, DataSet, Method, StudyResult
from ga4gh.vrs.models import MolecularVariation
from pydantic import Field


class ExperimentalVariantFunctionalImpactStudyResult(StudyResultBase):
    """A StudyResult that reports a functional impact score from a variant functional assay or study."""

    type: Literal["ExperimentalVariantFunctionalImpactStudyResult"] = Field(
        "ExperimentalVariantFunctionalImpactStudyResult",
        description="MUST be 'ExperimentalVariantFunctionalImpactStudyResult'.",
    )
    focusVariant: MolecularVariation | iriReference = Field(
        ...,
        description="The genetic variant for which a functional impact score is generated.",
    )
    functionalImpactScore: float | None = Field(
        None,
        description="The score of the variant impact measured in the assay or study.",
    )
    specifiedBy: Method | iriReference | None = Field(
        None,
        description="The assay that was performed to generate the reported functional impact score.",
    )
    sourceDataSet: DataSet | None = Field(
        None,
        description="The full data set that provided the reported the functional impact score. ",
    )
