"""VA Spec Shared Domain Entity Data Structures"""

from __future__ import annotations

from typing import ClassVar

from pydantic import Field

from ga4gh.core.metadata import Maturity
from ga4gh.core.models import (
    ConceptSet,
    MappableConcept,
    MembershipOperator,
    iriReference,
)
from ga4gh.va_spec.base.metadata import BaseMetadataMixin


class ConditionSet(BaseMetadataMixin, ConceptSet):
    """A specialization of ConceptSet representing a set of conditions (diseases,
    phenotypes, traits) that occur together or are related, depending on the membership
    operator. Concepts are restricted to Condition and ConditionSet members.
    """

    _maturity: ClassVar[Maturity] = Maturity.TRIAL_USE

    concepts: list[Condition | ConditionSet | iriReference] = Field(
        ...,
        min_length=2,
        description="A list of conditions (diseases, phenotypes, traits) that are co-occurring or related, depending on the membership operator.",
    )
    membershipOperator: MembershipOperator = Field(
        ...,
        description="The logical relationship between members of the set, that indicates how they manifest in patients/research subjects. The value 'AND' indicates that all conditions in the set co-occur together in a given patient or subject. The value 'OR' indicates that only one condition in the set manifests in each participant interrogated in a given study.",
    )


class Condition(BaseMetadataMixin, MappableConcept):
    """A specialization of MappableConcept representing a single condition (disease,
    phenotype, or trait).

    Allowed conceptType values include: Condition, Phenotype,
    Disease, Trait, Absent.
    """

    _maturity: ClassVar[Maturity] = Maturity.TRIAL_USE

    conceptType: str = Field(
        default="Condition",
        description="A term indicating the type of concept being represented by the MappableConcept.",
    )


class TherapyGroup(BaseMetadataMixin, ConceptSet):
    """A specialization of ConceptSet representing a group of two or more therapies that
    are applied in combination to a single patient/subject, or applied individually to a
    different subset of participants in a research study.

    Concepts are restricted to Therapy and TherapyGroup members.
    """

    _maturity: ClassVar[Maturity] = Maturity.TRIAL_USE

    concepts: list[Therapy | TherapyGroup | iriReference] = Field(
        ...,
        min_length=2,
        description="A list of therapies that are applied to treat a condition.",
    )
    membershipOperator: MembershipOperator = Field(
        ...,
        description="The logical relationship between members of the group, that indicates how they were applied in treating participants in a study. The value 'AND' indicates that all therapies in the group were applied in combination to a given patient or subject. The value 'OR' indicates that each therapy was applied individually to a distinct subset of participants in the cohort that was interrogated in a given study.",
    )


class Therapy(BaseMetadataMixin, MappableConcept):
    """A specialization of MappableConcept representing an individual therapy (drug,
    procedure, behavioral intervention, etc.).

    Allowed conceptType values include: Therapy, Absent, Drug, Procedure, Behavioral
    Intervention.
    """

    _maturity: ClassVar[Maturity] = Maturity.TRIAL_USE

    conceptType: str = Field(
        default="Therapy",
        description="A term indicating the type of concept being represented by the MappableConcept.",
    )
