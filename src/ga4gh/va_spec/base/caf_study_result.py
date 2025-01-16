"""Cohort Allele Frequency Study Result Standard Profile"""

from typing import Literal

from ga4gh.core.models import iriReference
from ga4gh.va_spec.base.core import DataSet, StudyGroup, StudyResult
from ga4gh.vrs.models import Allele
from pydantic import Field


class CohortAlleleFrequencyStudyResult(StudyResult):
    """A StudyResult that reports measures related to the frequency of an Allele in a cohort"""

    type: Literal["CohortAlleleFrequencyStudyResult"] = Field(
        "CohortAlleleFrequencyStudyResult",
        description="MUST be 'CohortAlleleFrequencyStudyResult'.",
    )
    sourceDataSet: DataSet | None = Field(
        None,
        description="The dataset from which the CohortAlleleFrequencyStudyResult was reported.",
    )
    focusAllele: Allele | iriReference = Field(
        ..., description="The Allele for which frequency results are reported."
    )
    focusAlleleCount: int = Field(
        ..., description="The number of occurrences of the focusAllele in the cohort."
    )
    locusAlleleCount: int = Field(
        ...,
        description="The number of occurrences of all alleles at the locus in the cohort.",
    )
    focusAlleleFrequency: int = Field(
        ..., description="The frequency of the focusAllele in the cohort."
    )
    cohort: StudyGroup = Field(
        ..., description="The cohort from which the frequency was derived."
    )
    subCohortFrequency: list["CohortAlleleFrequencyStudyResult"] | None = Field(
        None,
        description="A list of CohortAlleleFrequency objects describing subcohorts of the cohort currently being described. Subcohorts can be further subdivided into more subcohorts. This enables, for example, the description of different ancestry groups and sexes among those ancestry groups.",
    )
    ancillaryResults: dict | None = None
    qualityMeasures: dict | None = None


CohortAlleleFrequencyStudyResult.model_rebuild()
