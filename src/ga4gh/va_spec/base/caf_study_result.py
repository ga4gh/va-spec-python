"""Cohort Allele Frequency Study Result Standard Profile"""

from __future__ import annotations

from typing import Any, Literal

from ga4gh.core.models import iriReference
from ga4gh.va_spec.base.core import DataSet, StudyGroup, StudyResult
from ga4gh.vrs.models import Allele
from pydantic import Field, field_validator


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
    focus: None = Field(
        None, exclude=True, repr=False
    )  # extends property in JSON Schema. Should not be used
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
    focusAlleleFrequency: float = Field(
        ..., description="The frequency of the focusAllele in the cohort."
    )
    cohort: StudyGroup = Field(
        ..., description="The cohort from which the frequency was derived."
    )
    subCohortFrequency: list[CohortAlleleFrequencyStudyResult] | None = Field(
        None,
        description="A list of CohortAlleleFrequency objects describing subcohorts of the cohort currently being described. Subcohorts can be further subdivided into more subcohorts. This enables, for example, the description  of different ancestry groups and sexes among those ancestry groups.",
    )
    ancillaryResults: dict | None = None
    qualityMeasures: dict | None = None

    def __getattribute__(self, name: str) -> Any:  # noqa: ANN401
        """Retrieve the value of the specified attribute

        :param name: Name of attribute being accessed
        :return: The value of the specified attribute
        :raises ValueError: If the attribute being accessed is not already defined in
            CohortAlleleFrequencyStudyResult or the attribute is `focus`
        """
        if name == "focus":
            err_msg = f"'{type(self).__name__!r}' object has no attribute '{name!r}'"
            raise AttributeError(err_msg)
        return super().__getattribute__(name)

    @field_validator("focus", mode="before")
    def set_focus_to_none(cls, v: Any) -> None:  # noqa: ANN401, N805
        """Set focus to None"""
        return


del CohortAlleleFrequencyStudyResult.model_fields[
    "focus"
]  # Need to remove inherited property
