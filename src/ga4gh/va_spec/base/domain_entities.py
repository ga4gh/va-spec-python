"""VA Spec Shared Domain Entity Data Structures"""

from ga4gh.core.models import BaseModelForbidExtra, Element, MappableConcept
from ga4gh.va_spec.base.enums import MembershipOperator
from pydantic import ConfigDict, Field, RootModel


class ConditionSet(Element, BaseModelForbidExtra):
    """A set of conditions (diseases, phenotypes, traits).
    A set of two or more conditions that co-occur in the same patient/subject, or are
    manifest individually in a different subset of participants in a research study.
    """

    model_config = ConfigDict(use_enum_values=True)

    conditions: list[MappableConcept] = Field(
        ...,
        min_length=2,
        description="A list of conditions (diseases, phenotypes, traits) that are co-occurring.",
    )
    membershipOperator: MembershipOperator = Field(
        ...,
        description="The logical relationship between members of the set, that indicates how they manifest in patients/research subjects. The value 'AND' indicates that all conditions in the set co-occur together in a given patient or subject. The value 'OR' indicates that only one condition in the set manifests in each participant interrogated in a given study.",
    )


class Condition(RootModel):
    """A single condition (disease, phenotype, or trait), or a set of conditions
    (ConditionSet).
    """

    root: ConditionSet | MappableConcept = Field(
        ...,
        json_schema_extra={
            "description": "A single condition (disease, phenotype, or trait), or a set of conditions (ConditionSet)."
        },
    )


class TherapyGroup(Element, BaseModelForbidExtra):
    """A group of two or more therapies that are applied in combination to a single
    patient/subject, or applied individually to a different subset of participants in a
    research study
    """

    model_config = ConfigDict(use_enum_values=True)

    therapies: list[MappableConcept] = Field(
        ...,
        min_length=2,
        description="A list of therapies that are applied to treat a condition.",
    )
    membershipOperator: MembershipOperator = Field(
        ...,
        description="The logical relationship between members of the group, that indicates how they were applied in treating participants in a study.  The value 'AND' indicates that all therapies in the group were applied in combination to a given patient or subject. The value 'OR' indicates that each therapy was applied individually to a distinct subset of participants in the cohort that was interrogated in a given study.",
    )


class Therapeutic(RootModel):
    """An individual therapy (drug, procedure, behavioral intervention, etc.), or group of therapies (TherapyGroup)."""

    root: TherapyGroup | MappableConcept = Field(
        ...,
        json_schema_extra={
            "description": "An individual therapy (drug, procedure, behavioral intervention, etc.), or group of therapies (TherapyGroup)."
        },
    )
