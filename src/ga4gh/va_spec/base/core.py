"""VA Spec Base Core Models"""

from __future__ import annotations

import importlib
import inspect
from abc import ABC
from datetime import date
from enum import Enum
from typing import Annotated, Literal, TypeVar

from ga4gh.cat_vrs.models import CategoricalVariant
from ga4gh.core.models import (
    BaseModelForbidExtra,
    Entity,
    MappableConcept,
    iriReference,
)
from ga4gh.va_spec.base.domain_entities import Condition, Therapeutic
from ga4gh.vrs.models import Allele, MolecularVariation
from pydantic import (
    ConfigDict,
    Field,
    RootModel,
    StringConstraints,
    ValidationError,
    field_validator,
)

StatementType = TypeVar("StatementType", bound="Statement")

#########################################
# Abstract Core Classes
#########################################


class InformationEntity(Entity):
    """An abstract (non-physical) entity that represents 'information content' carried by
    physical or digital information artifacts such as books, web pages, data sets, or
    images.
    """

    specifiedBy: Method | iriReference | None = Field(
        None,
        description="A specification that describes all or part of the process that led to creation of the Information Entity",
    )
    contributions: list[Contribution] | None = Field(
        None,
        description="Specific actions taken by an Agent toward the creation, modification, validation, or deprecation of an Information Entity.",
    )
    reportedIn: list[Document] | iriReference | None = Field(
        None, description="A document in which the the Information Entity is reported."
    )


class _StudyResult(InformationEntity, ABC):
    """A collection of data items from a single study that pertain to a particular subject
    or experimental unit in the study, along with optional provenance information
    describing how these data items were generated.
    """

    sourceDataSet: DataSet | None = Field(
        None,
        description="A larger DataSet from which the data included in the StudyResult was taken or derived.",
    )


class Proposition(Entity):
    """An abstract entity representing a possible fact that may be true or false. As
    abstract entities, Propositions capture a 'sharable' piece of meaning whose identify
    and existence is independent of space and time, or whether it is ever asserted to be
    true by some agent.
    """

    subject: dict = Field(
        ..., description="The Entity or concept about which the Proposition is made."
    )
    predicate: str = Field(
        ...,
        description="The relationship declared to hold between the subject and the object of the Proposition.",
    )
    object: dict = Field(
        ...,
        description="An Entity or concept that is related to the subject of a Proposition via its predicate.",
    )


class SubjectVariantProposition(RootModel):
    """A `Proposition` that has a variant as the subject."""

    root: (
        ExperimentalVariantFunctionalImpactProposition
        | VariantPathogenicityProposition
        | VariantDiagnosticProposition
        | VariantPrognosticProposition
        | VariantOncogenicityProposition
        | VariantTherapeuticResponseProposition
    ) = Field(discriminator="type")


class _SubjectVariantPropositionBase(Entity, ABC):
    subjectVariant: MolecularVariation | CategoricalVariant | iriReference = Field(
        ..., description="A variant that is the subject of the Proposition."
    )


class ClinicalVariantProposition(_SubjectVariantPropositionBase):
    """A proposition for use in describing the effect of variants in human subjects."""

    geneContextQualifier: MappableConcept | iriReference | None = Field(
        None,
        description="Reports a gene impacted by the variant, which may contribute to the association described in the Proposition.",
    )
    alleleOriginQualifier: MappableConcept | iriReference | None = Field(
        None,
        description="Reports whether the Proposition should be interpreted in the context of an inherited (germline) variant, an acquired (somatic) mutation, or another more nuanced concept.",
    )


class ExperimentalVariantFunctionalImpactProposition(
    _SubjectVariantPropositionBase, BaseModelForbidExtra
):
    """A Proposition describing the impact of a variant on the function sequence feature
    (typically a gene or gene product).
    """

    type: Literal["ExperimentalVariantFunctionalImpactProposition"] = Field(
        "ExperimentalVariantFunctionalImpactProposition",
        description="MUST be 'ExperimentalVariantFunctionalImpactProposition'.",
    )
    predicate: str = Field(
        "impactsFunctionOf",
        description="The relationship the Proposition describes between the subject variant and object sequence feature whose function it may alter.",
    )
    objectSequenceFeature: iriReference | MappableConcept = Field(
        ...,
        description="The sequence feature (typically a gene or gene product) on whose function the impact of the subject variant is reported.",
    )
    experimentalContextQualifier: iriReference | Document | dict | None = Field(
        None,
        description="An assay in which the reported variant functional impact was determined - providing a specific experimental context in which this effect is asserted to hold.",
    )


class DiagnosticPredicate(str, Enum):
    """Define constraints for diagnostic predicate"""

    INCLUSIVE = "isDiagnosticInclusionCriterionFor"
    EXCLUSIVE = "isDiagnosticExclusionCriterionFor"


class VariantDiagnosticProposition(ClinicalVariantProposition, BaseModelForbidExtra):
    """A Proposition about whether a variant is associated with a disease (a diagnostic
    inclusion criterion), or absence of a disease (diagnostic exclusion criterion).
    """

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["VariantDiagnosticProposition"] = Field(
        "VariantDiagnosticProposition",
        description="MUST be 'VariantDiagnosticProposition'.",
    )
    predicate: DiagnosticPredicate
    objectCondition: Condition | iriReference = Field(
        ..., description="The disease that is evaluated for diagnosis."
    )


class VariantOncogenicityProposition(ClinicalVariantProposition, BaseModelForbidExtra):
    """A proposition describing the role of a variant in causing a tumor type."""

    type: Literal["VariantOncogenicityProposition"] = Field(
        "VariantOncogenicityProposition",
        description="MUST be 'VariantOncogenicityProposition'.",
    )
    predicate: str = "isCausalFor"
    objectTumorType: Condition | iriReference = Field(
        ..., description="The tumor type for which the variant impact is evaluated."
    )


class VariantPathogenicityProposition(ClinicalVariantProposition, BaseModelForbidExtra):
    """A proposition describing the role of a variant in causing a heritable condition."""

    type: Literal["VariantPathogenicityProposition"] = Field(
        "VariantPathogenicityProposition",
        description="Must be 'VariantPathogenicityProposition'",
    )
    predicate: str = "isCausalFor"
    objectCondition: Condition | iriReference = Field(
        ..., description="The Condition for which the variant impact is stated."
    )
    penetranceQualifier: MappableConcept | None = Field(
        None,
        description="Reports the penetrance of the pathogenic effect - i.e. the extent to which the variant impact is expressed by individuals carrying it as a measure of the proportion of carriers exhibiting the condition.",
    )
    modeOfInheritanceQualifier: MappableConcept | None = Field(
        None,
        description="Reports a pattern of inheritance expected for the pathogenic effect of the variant. HPO terms within the hierarchy of 'HP:0000005' (mode of inheritance) are recommended to specify.",
    )


class PrognosticPredicate(str, Enum):
    """Define constraints for prognostic predicate"""

    BETTER_OUTCOME = "associatedWithBetterOutcomeFor"
    WORSE_OUTCOME = "associatedWithWorseOutcomeFor"


class VariantPrognosticProposition(ClinicalVariantProposition, BaseModelForbidExtra):
    """A Proposition about whether a variant is associated with an improved or worse outcome for a disease."""

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["VariantPrognosticProposition"] = Field(
        "VariantPrognosticProposition",
        description="MUST be 'VariantPrognosticProposition'.",
    )
    predicate: PrognosticPredicate
    objectCondition: Condition | iriReference = Field(
        ..., description="The disease that is evaluated for outcome."
    )


class TherapeuticResponsePredicate(str, Enum):
    """Define constraints for therapeutic response predicate"""

    SENSITIVITY = "predictsSensitivityTo"
    RESISTANCE = "predictsResistanceTo"


class VariantTherapeuticResponseProposition(
    ClinicalVariantProposition, BaseModelForbidExtra
):
    """A Proposition about the role of a variant in modulating the response of a neoplasm to drug
    administration or other therapeutic procedures.
    """

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["VariantTherapeuticResponseProposition"] = Field(
        "VariantTherapeuticResponseProposition",
        description="MUST be 'VariantTherapeuticResponseProposition'.",
    )
    predicate: TherapeuticResponsePredicate
    objectTherapeutic: Therapeutic | iriReference = Field(
        ...,
        description="A drug administration or other therapeutic procedure that the neoplasm is intended to respond to.",
    )
    conditionQualifier: Condition | iriReference = Field(
        ...,
        description="Reports the disease context in which the variant's association with therapeutic sensitivity or resistance is evaluated. Note that this is a required qualifier in therapeutic response propositions.",
    )


#########################################
# Concrete Core Classes
#########################################


class CoreType(str, Enum):
    """Define VA Spec Base Core Types"""

    METHOD = "Method"
    CONTRIBUTION = "Contribution"
    DOCUMENT = "Document"
    AGENT = "Agent"
    STATEMENT = "Statement"
    EVIDENCE_LINE = "EvidenceLine"
    DATA_SET = "DataSet"
    STUDY_GROUP = "StudyGroup"


class Method(Entity, BaseModelForbidExtra):
    """A set of instructions that specify how to achieve some objective."""

    type: Literal["Method"] = Field(
        CoreType.METHOD.value, description=f"MUST be '{CoreType.METHOD.value}'."
    )
    subtype: MappableConcept | None = Field(
        None,
        description="A specific type of method that a Method instance represents (e.g. 'Variant Interpretation Guideline', or 'Experimental Protocol').",
    )
    reportedIn: Document | iriReference | None = Field(
        None, description="A document in which the the Method is reported."
    )


class Contribution(Entity, BaseModelForbidExtra):
    """An action taken by an agent in contributing to the creation, modification,
    assessment, or deprecation of a particular entity (e.g. a Statement, EvidenceLine,
    DataSet, Publication, etc.)
    """

    type: Literal["Contribution"] = Field(
        CoreType.CONTRIBUTION.value,
        description=f"MUST be '{CoreType.CONTRIBUTION.value}'.",
    )
    contributor: Agent | None = Field(
        None, description="The agent that made the contribution."
    )
    activityType: MappableConcept | None = Field(
        None,
        description="The specific type of activity performed or role played by an agent in making the contribution (e.g. for a publication, agents may contribute as a primary author, editor, figure designer, data generator, etc.). Values of this property may be framed as activities, or as contribution roles (e.g. using terms from the Contribution Role Ontology (CRO)).",
    )
    date: date | None


class Document(Entity, BaseModelForbidExtra):
    """A collection of information, usually in a text-based or graphic human-readable
    form, intended to be read and understood together as a whole.
    """

    type: Literal["Document"] = Field(
        CoreType.DOCUMENT.value, description=f"Must be '{CoreType.DOCUMENT.value}'"
    )
    subtype: MappableConcept | None = Field(
        None,
        description="A specific type of document that a Document instance represents (e.g.  'publication', 'patent', 'pathology report')",
    )
    title: str | None = Field(
        None, description="The official title given to the document by its authors."
    )
    urls: (
        list[Annotated[str, StringConstraints(pattern=r"^(https?|s?ftp)://")]] | None
    ) = Field(
        None,
        description="One or more URLs from which the content of the Document can be retrieved.",
    )
    doi: (
        Annotated[str, StringConstraints(pattern=r"^10\.(\d+)(\.\d+)*\/[\w\-\.]+")]
        | None
    ) = Field(
        None,
        description="A [Digital Object Identifier](https://www.doi.org/the-identifier/what-is-a-doi/) for the document.",
    )
    pmid: int | None = Field(
        None,
        description="A [PubMed unique identifier](https://en.wikipedia.org/wiki/PubMed#PubMed_identifier) for the document.",
    )


class Agent(Entity, BaseModelForbidExtra):
    """An autonomous actor (person, organization, or software agent) that bears some
    form of responsibility for an activity taking place, for the existence of an entity,
    or for another agent's activity.
    """

    type: Literal["Agent"] = Field(
        CoreType.AGENT.value, description=f"MUST be '{CoreType.AGENT.value}'."
    )
    name: str | None = Field(None, description="The given name of the Agent.")
    subtype: MappableConcept | None = Field(
        None,
        description="A specific type of agent the Agent object represents. Recommended subtypes include codes for `person`, `organization`, or `software`.",
    )


class Direction(str, Enum):
    """A term indicating whether the Statement supports, disputes, or remains neutral
    w.r.t. the validity of the Proposition it evaluates.
    """

    SUPPORTS = "supports"
    NEUTRAL = "neutral"
    DISPUTES = "disputes"


class DataSet(Entity, BaseModelForbidExtra):
    """A collection of related data items or records that are organized together in a
    common format or structure, to enable their computational manipulation as a unit.
    """

    type: Literal["DataSet"] = Field(
        CoreType.DATA_SET.value, description=f"MUST be '{CoreType.DATA_SET.value}'."
    )
    subtype: MappableConcept | None = Field(
        None,
        description="A specific type of data set the DataSet instance represents (e.g. a 'clinical data set', a 'sequencing data set', a 'gene expression data set', a 'genome annotation data set')",
    )
    reportedIn: Document | iriReference | None = Field(
        None, description="A document in which the the Method is reported."
    )
    releaseDate: date | None = Field(
        None,
        description="Indicates the date a version of a DataSet was formally released.",
    )
    version: str | None = Field(
        None, description="The version of the DataSet, as assigned by its creator."
    )
    license: MappableConcept | None = Field(
        None,
        description="A specific license that dictates legal permissions for how a data set can be used (by whom, where, for what purposes, with what additional requirements, etc.)",
    )


class EvidenceLine(InformationEntity, BaseModelForbidExtra):
    """An independent, evidence-based argument that may support or refute the validity
    of a specific Proposition. The strength and direction of this argument is based on
    an interpretation of one or more pieces of information as evidence for or against
    the target Proposition.
    """

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["EvidenceLine"] = Field(
        CoreType.EVIDENCE_LINE.value,
        description=f"MUST be '{CoreType.EVIDENCE_LINE.value}'.",
    )
    targetProposition: Proposition | None = Field(
        None,
        description="The possible fact against which evidence items contained in an Evidence Line were collectively evaluated, in determining the overall strength and direction of support they provide. For example, in an ACMG Guideline-based assessment of variant pathogenicity, the support provided by distinct lines of evidence are assessed against a target proposition that the variant is pathogenic for a specific disease.",
    )
    hasEvidenceItems: (
        list[StudyResult | StatementType | EvidenceLine | iriReference] | None
    ) = Field(
        None,
        description="An individual piece of information that was evaluated as evidence in building the argument represented by an Evidence Line.",
    )
    directionOfEvidenceProvided: Direction = Field(
        ...,
        description="The direction of support that the Evidence Line is determined to provide toward its target Proposition (supports, disputes, neutral)",
    )
    strengthOfEvidenceProvided: MappableConcept | None = Field(
        None,
        description="The strength of support that an Evidence Line is determined to provide for or against its target Proposition, evaluated relative to the direction indicated by the directionOfEvidenceProvided value.",
    )
    scoreOfEvidenceProvided: float | None = Field(
        None,
        description="A quantitative score indicating the strength of support that an Evidence Line is determined to provide for or against its target Proposition, evaluated relative to the direction indicated by the directionOfEvidenceProvided value.",
    )
    evidenceOutcome: MappableConcept | None = Field(
        None,
        description="A term summarizing the overall outcome of the evidence assessment represented by the Evidence Line, in terms of the direction and strength of support it provides for or against the target Proposition.",
    )

    @field_validator("hasEvidenceItems", mode="before")
    def validate_has_evidence_items(
        cls,  # noqa: N805
        v: list[StudyResult, StatementType, EvidenceLine, iriReference] | None,
    ) -> list | None:
        """Ensure hasEvidenceItems is correct type

        This is needed since Pydantic was unable to determine which model to use

        This only handles cases defined in the VA-Spec.

        :param v: hasEvidenceItems value
        :raises ValueError: If unable to find valid model for evidence items
        :return: Evidence items
        """
        if not v:
            return v

        evidence_items = []

        # Avoid circular imports
        aac_2017_module = importlib.import_module("ga4gh.va_spec.aac_2017.models")
        has_evidence_items_models = [
            obj_
            for _, obj_ in vars(aac_2017_module).items()
            if inspect.isclass(obj_)
            and issubclass(obj_, Statement)
            and obj_ is not Statement
        ]
        has_evidence_items_models.extend(
            [Statement, StudyResult, EvidenceLine, iriReference]
        )

        for evidence_item in v:
            if isinstance(evidence_item, dict):
                found_model = False
                for evidence_item_model in has_evidence_items_models:
                    try:
                        evidence_item = evidence_item_model(**evidence_item)
                    except ValidationError:
                        pass
                    else:
                        evidence_items.append(evidence_item)
                        found_model = True
                        break
                if not found_model:
                    err_msg = "Unable to find valid model"
                    raise ValueError(err_msg)
            else:
                evidence_items.append(evidence_item)
        return evidence_items


class Statement(InformationEntity, BaseModelForbidExtra):
    """A claim of purported truth as made by a particular agent, on a particular
    occasion. Statements may be used to put forth a possible fact (i.e. a 'Proposition')
    as true or false, or to provide a more nuanced assessment of the level of confidence
    or evidence supporting a particular Proposition.
    """

    model_config = ConfigDict(use_enum_values=True)

    type: Literal["Statement"] = Field(
        CoreType.STATEMENT.value, description=f"MUST be '{CoreType.STATEMENT.value}'."
    )
    proposition: Proposition = Field(
        ...,
        description="A possible fact, the validity of which is assessed and reported by the Statement. A Statement can put forth the proposition as being true, false, or uncertain, and may provide an assessment of the level of confidence/evidence supporting this claim.",
    )
    direction: Direction = Field(
        ...,
        description="A term indicating whether the Statement supports, disputes, or remains neutral w.r.t. the validity of the Proposition it evaluates.",
    )
    strength: MappableConcept | None = Field(
        None,
        description="A term used to report the strength of a Proposition's assessment in the direction indicated (i.e. how strongly supported or disputed the Proposition is believed to be).  Implementers may choose to frame a strength assessment in terms of how *confident* an agent is that the Proposition is true or false, or in terms of the *strength of all evidence* they believe supports or disputes it.",
    )
    score: float | None = Field(
        None,
        description="A quantitative score that indicates the strength of a Proposition's assessment in the direction indicated (i.e. how strongly supported or disputed the Proposition is believed to be). Depending on its implementation, a score may reflect how *confident* that agent is that the Proposition is true or false, or the *strength of evidence* they believe supports or disputes it. Instructions for how to interpret the menaing of a given score may be gleaned from the method or document referenced in 'specifiedBy' attribute.",
    )
    classification: MappableConcept | None = Field(
        None,
        description="A single term or phrase summarizing the outcome of direction and strength assessments of a Statement's Proposition, in terms of a classification of its subject.",
    )
    hasEvidenceLines: list[EvidenceLine | iriReference] | None = Field(
        None,
        description="An evidence-based argument that supports or disputes the validity of the proposition that a Statement assesses or puts forth as true. The strength and direction of this argument (whether it supports or disputes the proposition, and how strongly) is based on an interpretation of one or more pieces of information as evidence (i.e. 'Evidence Items).",
    )


class StudyGroup(Entity, BaseModelForbidExtra):
    """A collection of individuals or specimens from the same taxonomic class, selected
    for analysis in a scientific study based on their exhibiting one or more common
    characteristics  (e.g. species, race, age, gender, disease state, income). May be
    referred to as a 'cohort' or 'population' in specific research settings.
    """

    type: Literal["StudyGroup"] = Field(
        CoreType.STUDY_GROUP.value,
        description=f"Must be '{CoreType.STUDY_GROUP.value}'",
    )
    memberCount: int | None = Field(
        None, description="The total number of individual members in the StudyGroup."
    )
    characteristics: list[MappableConcept] | None = Field(
        None,
        description="A feature or role shared by all members of the StudyGroup, representing a criterion for membership in the group.",
    )


class CohortAlleleFrequencyStudyResult(_StudyResult, BaseModelForbidExtra):
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
    focusAlleleFrequency: float = Field(
        ..., description="The frequency of the focusAllele in the cohort."
    )
    cohort: StudyGroup = Field(
        ..., description="The cohort from which the frequency was derived."
    )
    subCohortFrequency: list[CohortAlleleFrequencyStudyResult] | None = Field(
        None,
        description="A list of CohortAlleleFrequency objects describing subcohorts of the cohort currently being described. Subcohorts can be further subdivided into more subcohorts. This enables, for example, the description of different ancestry groups and sexes among those ancestry groups.",
    )
    ancillaryResults: dict | None = None
    qualityMeasures: dict | None = None


class ExperimentalVariantFunctionalImpactStudyResult(
    _StudyResult, BaseModelForbidExtra
):
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
        description="The full data set that provided the reported the functional impact score.",
    )


class StudyResult(RootModel):
    """A collection of data items from a single study that pertain to a particular subject
    or experimental unit in the study, along with optional provenance information
    describing how these data items were generated.
    """

    root: (
        CohortAlleleFrequencyStudyResult
        | ExperimentalVariantFunctionalImpactStudyResult
    ) = Field(
        ...,
        json_schema_extra={
            "description": "A collection of data items from a single study that pertain to a particular subject or experimental unit in the study, along with optional provenance information describing how these data items were generated."
        },
        discriminator="type",
    )
