"""Cohort Allele Frequency Study Result Standard Profile"""

from typing import Any, Literal

from ga4gh.core.models import iriReference
from ga4gh.va_spec.base.core import DataSet, Method, StudyResult
from ga4gh.vrs.models import MolecularVariation
from pydantic import Field, field_validator


class ExperimentalVariantFunctionalImpactStudyResult(StudyResult):
    """A StudyResult that reports a functional impact score from a variant functional assay or study."""

    type: Literal["ExperimentalVariantFunctionalImpactStudyResult"] = Field(
        "ExperimentalVariantFunctionalImpactStudyResult",
        description="MUST be 'ExperimentalVariantFunctionalImpactStudyResult'.",
    )
    focus: None = Field(
        None, exclude=True, repr=False
    )  # extends property in JSON Schema. Should not be used
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

    def __getattribute__(self, name: str) -> Any:  # noqa: ANN401
        """Retrieve the value of the specified attribute

        :param name: Name of attribute being accessed
        :return: The value of the specified attribute
        :raises ValueError: If the attribute being accessed is not already defined in
            ExperimentalVariantFunctionalImpactStudyResult or the attribute is `focus`
        """
        if name == "focus":
            err_msg = f"'{type(self).__name__!r}' object has no attribute '{name!r}'"
            raise AttributeError(err_msg)
        return super().__getattribute__(name)

    @field_validator("focus", mode="before")
    def set_focus_to_none(cls, v: Any) -> None:  # noqa: ANN401, N805
        """Set focus to None"""
        return


del ExperimentalVariantFunctionalImpactStudyResult.model_fields[
    "focus"
]  # Need to remove inherited property
