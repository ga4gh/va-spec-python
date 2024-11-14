"""VA Spec Cohort Allele Frequency (population frequency) Study Result Standard Profile"""

from __future__ import annotations

from typing import Literal

from ga4gh.core.entity_models import (
    DataSet,
    StudyGroup,
    StudyResultBase,
)
from ga4gh.vrs.models import Allele
from pydantic import ConfigDict, Field


class CohortAlleleFrequencyStudyResult(StudyResultBase):
    """A StudyResult that reports measures related to the frequency of an Allele in a cohort"""

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["CohortAlleleFrequencyStudyResult"] = Field(
        "CohortAlleleFrequencyStudyResult",
        description="MUST be 'CohortAlleleFrequencyStudyResult'.",
    )
    sourceDataSet: list[DataSet] | None = Field(
        None,
        description="The dataset from which the CohortAlleleFrequencyStudyResult was reported.",
    )
    focusAllele: Allele | str = Field(
        ...,
        description="The specific subject or experimental unit in a Study that data in the StudyResult object is about - e.g. a particular variant in a population allele frequency dataset like ExAC or gnomAD.",
    )
    focusAlleleCount: int = Field(
        ..., description="The number of occurrences of the focusAllele in the cohort."
    )
    locusAlleleCount: int = Field(
        ...,
        description="The number of occurrences of all alleles at the locus in the cohort (sometimes referred to as 'allele number')",
    )
    focusAlleleFrequency: float = Field(
        ..., description="The frequency of the focusAllele in the cohort."
    )
    cohort: list[StudyGroup] = Field(
        ..., description="The cohort from which the frequency was derived."
    )
    subCohortFrequency: list[CohortAlleleFrequencyStudyResult] | None = Field(
        None,
        description="A list of CohortAlleleFrequency objects describing subcohorts of the cohort currently being described. This creates a recursive relationship and subcohorts can be further subdivided into more subcohorts. This enables, for example, the description of different ancestry groups and sexes among those ancestry groups.",
    )
