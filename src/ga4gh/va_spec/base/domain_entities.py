"""VA Spec Shared Domain Entity Data Structures"""

from ga4gh.core.models import BaseModelForbidExtra, Element, MappableConcept
from pydantic import Field, RootModel


class TraitSet(Element, BaseModelForbidExtra):
    """A set of conditions (diseases, phenotypes, traits) that are co-occurring."""

    traits: list[MappableConcept] | None = Field(
        None,
        min_length=2,
        description="A list of conditions (diseases, phenotypes, traits) that are co-occurring.",
    )


class Condition(RootModel):
    """A set of traits (TraitSet) or a single trait (Disease, Phenotype, etc.) that
    represents the object of a Variant Pathogenicity statement.
    """

    root: TraitSet | MappableConcept = Field(
        ...,
        json_schema_extra={
            "description": "A set of traits (TraitSet) or a single trait (Disease, Phenotype, etc.) that represents the object of a Variant Pathogenicity statement."
        },
    )


class TherapyGroup(Element, BaseModelForbidExtra):
    """A group of therapies that are applied together to treat a condition."""

    therapies: list[MappableConcept] | None = Field(
        None,
        min_length=2,
        description="A list of therapies that are applied together to treat a condition.",
    )
    groupType: MappableConcept | None = Field(
        None, description="The type of the therapy group."
    )


class Therapeutic(RootModel):
    """A group of therapies (TherapyGroup) or a single therapy (drug, procedure, behavioral intervention, etc.)."""

    root: TherapyGroup | MappableConcept = Field(
        ...,
        json_schema_extra={
            "description": "A group of therapies (TherapyGroup) or a single therapy (drug, procedure, behavioral intervention, etc.)."
        },
    )
