"""Test VA Spec Pydantic model"""

import json
from copy import deepcopy

import pytest
import yaml
from pydantic import ValidationError
from tests.conftest import SUBMODULES_DIR

from ga4gh.core.models import Coding, MappableConcept, code, iriReference
from ga4gh.va_spec import acmg_2015, base, ccv_2022
from ga4gh.va_spec.aac_2017.models import VariantClinicalSignificanceStatement
from ga4gh.va_spec.acmg_2015.models import (
    VariantPathogenicityEvidenceLine,
    VariantPathogenicityStatement,
)
from ga4gh.va_spec.base import (
    Agent,
    CohortAlleleFrequencyStudyResult,
    ExperimentalVariantFunctionalImpactStudyResult,
    TherapyGroup,
    TumorVariantFrequencyStudyResult,
)
from ga4gh.va_spec.base.core import (
    Direction,
    EvidenceLine,
    InformationEntity,
    Method,
    Proposition,
    Statement,
    StudyGroup,
    VariantClinicalSignificanceProposition,
    VariantDiagnosticProposition,
    VariantOncogenicityProposition,
    VariantPathogenicityProposition,
    VariantPrognosticProposition,
    VariantTherapeuticResponseProposition,
)
from ga4gh.va_spec.base.domain_entities import ConditionSet
from ga4gh.va_spec.ccv_2022.models import (
    VariantOncogenicityEvidenceLine,
    VariantOncogenicityStatement,
)

VA_SPEC_TESTS_DIR = SUBMODULES_DIR / "tests"
VA_SPEC_TEST_FIXTURES = VA_SPEC_TESTS_DIR / "fixtures"


@pytest.fixture(scope="module")
def test_definitions():
    """Create test fixture for VA Spec test definitions"""
    with (VA_SPEC_TESTS_DIR / "test_definitions.yaml").open() as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def caf():
    """Create test fixture for CohortAlleleFrequencyStudyResult"""
    return CohortAlleleFrequencyStudyResult(
        focus="allele.json#/1",
        focusCount=0,
        alleleFrequency=0,
        locusCount=34086,
        cohort=StudyGroup(id="ALL", name="Overall"),
    )


@pytest.fixture()
def pathogenicity_evidence_line_params():
    """Return valid VariantPathogenicityEvidenceLine parameters."""
    return {
        "type": "EvidenceLine",
        "specifiedBy": {
            "type": "Method",
            "id": "PS3",
            "name": "ACMG 2015 PS3 Criterion",
            "reportedIn": {
                "type": "Document",
                "pmid": "25741868",
                "name": "ACMG Guidelines, 2015",
            },
            "methodType": "functional_data_assessment",
        },
        "directionOfEvidenceProvided": "supports",
        "evidenceOutcome": {
            "primaryCoding": {
                "code": "PS3_supporting",
                "system": "ACMG Guidelines, 2015",
            },
            "name": "ACMG 2015 PS3 Supporting Criterion Met",
        },
        "strengthOfEvidenceProvided": {
            "primaryCoding": {
                "system": "ACMG Guidelines, 2015",
                "code": "supporting",
            }
        },
    }


@pytest.fixture()
def oncogenicity_evidence_line_params():
    """Return valid VariantOncogenicityEvidenceLine parameters."""
    return {
        "type": "EvidenceLine",
        "specifiedBy": {
            "type": "Method",
            "reportedIn": {
                "type": "Document",
                "pmid": "35101336",
                "name": "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
            },
            "methodType": "functional_data_assessment",
        },
        "directionOfEvidenceProvided": "supports",
        "scoreOfEvidenceProvided": 1,
        "evidenceOutcome": {
            "primaryCoding": {
                "code": "OS2_supporting",
                "system": "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
            },
        },
        "strengthOfEvidenceProvided": {
            "primaryCoding": {
                "code": "supporting",
                "system": "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
            }
        },
    }


@pytest.mark.parametrize(
    ("proposition_class", "condition_field_name", "predicate"),
    [
        (
            VariantClinicalSignificanceProposition,
            "object",
            "hasClinicalSignificanceFor",
        ),
        (
            VariantDiagnosticProposition,
            "object",
            "isDiagnosticInclusionCriterionFor",
        ),
        (VariantOncogenicityProposition, "object", "isOncogenicFor"),
        (VariantPathogenicityProposition, "object", "isCausalFor"),
        (
            VariantPrognosticProposition,
            "object",
            "associatedWithBetterOutcomeFor",
        ),
        (
            VariantTherapeuticResponseProposition,
            "conditionQualifier",
            "predictsSensitivityTo",
        ),
    ],
)
def test_proposition_condition_helpers(
    proposition_class, condition_field_name, predicate
):
    """Test condition access without knowing the proposition field name."""
    initial_condition = iriReference(root="conditions.json#/1")
    proposition_data = {
        "subject": "alleles.json#/1",
        "predicate": predicate,
        condition_field_name: initial_condition,
    }
    if proposition_class is VariantTherapeuticResponseProposition:
        proposition_data["object"] = "therapeutics.json#/1"

    proposition = proposition_class(**proposition_data)

    assert proposition.condition == initial_condition
    assert proposition.condition == getattr(proposition, condition_field_name)
    assert "condition" not in proposition.model_dump()
    assert "condition" not in proposition_class.model_json_schema()["properties"]


def test_condition_set():
    """Ensure ConditionSet model works as expected"""
    condition_set_dict = {
        "membershipOperator": "AND",
        "concepts": [
            {
                "conceptType": "Disease",
                "id": "civic.did:3387",
                "mappings": [
                    {
                        "coding": {
                            "code": "DOID:0081279",
                            "system": "https://disease-ontology.org/?id=",
                        },
                        "relation": "exactMatch",
                    }
                ],
                "name": "Diffuse Astrocytoma, MYB- Or MYBL1-altered",
            },
            {
                "concepts": [
                    {
                        "conceptType": "Phenotype",
                        "id": "civic.phenotype:8121",
                        "mappings": [
                            {
                                "coding": {
                                    "code": "HP:0011463",
                                    "system": "https://hpo.jax.org/browse/term/",
                                },
                                "relation": "exactMatch",
                            }
                        ],
                        "name": "Childhood onset",
                    },
                    {
                        "conceptType": "Phenotype",
                        "id": "civic.phenotype:2656",
                        "mappings": [
                            {
                                "coding": {
                                    "code": "HP:0003621",
                                    "id": "HP:0003621",
                                    "system": "https://hpo.jax.org/browse/term/",
                                },
                                "relation": "exactMatch",
                            }
                        ],
                        "name": "Juvenile onset",
                    },
                    {
                        "conceptType": "Phenotype",
                        "id": "civic.phenotype:2643",
                        "mappings": [
                            {
                                "coding": {
                                    "code": "HP:0003581",
                                    "system": "https://hpo.jax.org/browse/term/",
                                },
                                "relation": "exactMatch",
                            }
                        ],
                        "name": "Adult onset",
                    },
                ],
                "membershipOperator": "OR",
            },
        ],
    }
    assert ConditionSet(**condition_set_dict)

    invalid_params = deepcopy(condition_set_dict)
    invalid_params["concepts"].pop()

    with pytest.raises(
        ValidationError, match="List should have at least 2 items after validation"
    ):
        ConditionSet(**invalid_params)


def test_agent():
    """Ensure Agent model works as expected"""
    agent = Agent(name="Joe")
    assert agent.type == "Agent"
    assert agent.name == "Joe"

    with pytest.raises(AttributeError, match="'Agent' object has no attribute 'label'"):
        agent.label  # noqa: B018

    with pytest.raises(ValueError, match='"Agent" object has no field "label"'):
        agent.label = "This is an agent"

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        Agent(name="Joe", label="Jane")


def test_caf_study_result(caf):
    """Ensure CohortAlleleFrequencyStudyResult model works as expected"""
    assert caf.focus.root == "allele.json#/1"
    assert caf.focusCount == 0
    assert caf.alleleFrequency == 0
    assert caf.locusCount == 34086
    assert caf.cohort.id == "ALL"
    assert caf.cohort.name == "Overall"
    assert caf.cohort.type == "StudyGroup"

    assert caf.model_dump()["focus"] == "allele.json#/1"
    assert json.loads(caf.model_dump_json())["focus"] == "allele.json#/1"


def test_experimental_func_impact_study_result():
    """Ensure ExperimentalVariantFunctionalImpactStudyResult model works as expected"""
    experimental_func_impact_study_result = (
        ExperimentalVariantFunctionalImpactStudyResult(focus="allele.json#/1")
    )
    assert experimental_func_impact_study_result.focus.root == "allele.json#/1"

    assert (
        experimental_func_impact_study_result.model_dump()["focus"] == "allele.json#/1"
    )
    assert "focus" in json.loads(
        experimental_func_impact_study_result.model_dump_json()
    )


def test_evidence_line(caf):
    """Ensure EvidenceLine model works as expected"""
    el_dict = {
        "type": "EvidenceLine",
        "hasEvidenceItems": [
            iriReference(root="evidence.json#/1"),
            {
                "id": "civic.eid:2997",
                "type": "Statement",
                "proposition": {
                    "type": "VariantTherapeuticResponseProposition",
                    "subject": {
                        "id": "civic.mpid:33",
                        "type": "CategoricalVariant",
                        "name": "EGFR L858R",
                    },
                    "geneContextQualifier": {
                        "id": "civic.gid:19",
                        "conceptType": "Gene",
                        "name": "EGFR",
                    },
                    "alleleOriginQualifier": {"name": "somatic"},
                    "predicate": "predictsSensitivityTo",
                    "object": {
                        "id": "civic.tid:146",
                        "conceptType": "Therapy",
                        "name": "Afatinib",
                    },
                    "conditionQualifier": {
                        "id": "civic.did:8",
                        "conceptType": "Disease",
                        "name": "Lung Non-small Cell Carcinoma",
                    },
                },
                "strength": {
                    "primaryCoding": {
                        "system": "AMP/ASCO/CAP Guidelines, 2017",
                        "code": "strong",
                    }
                },
                "classification": {
                    "primaryCoding": {
                        "system": "AMP/ASCO/CAP Guidelines, 2017",
                        "code": "tier i",
                    }
                },
                "specifiedBy": {
                    "id": "civic.method:2019",
                    "name": "CIViC Curation SOP (2019)",
                    "reportedIn": {
                        "name": "Danos et al., 2019, Genome Med.",
                        "title": "Standard operating procedure for curation and clinical interpretation of variants in cancer",
                        "doi": "10.1186/s13073-019-0687-x",
                        "pmid": "31779674",
                        "type": "Document",
                    },
                    "type": "Method",
                },
                "direction": "supports",
            },
        ],
        "directionOfEvidenceProvided": "disputes",
    }
    el = EvidenceLine(**el_dict)
    assert isinstance(el.hasEvidenceItems[0], iriReference)
    assert isinstance(el.hasEvidenceItems[1], InformationEntity)

    el_dict = {
        "type": "EvidenceLine",
        "hasEvidenceItems": [caf.model_dump(exclude_none=True)],
        "directionOfEvidenceProvided": "supports",
    }
    el = EvidenceLine(**el_dict)
    assert isinstance(el.hasEvidenceItems[0], InformationEntity)
    assert el.hasEvidenceItems[0].type == "CohortAlleleFrequencyStudyResult"

    el_dict = {
        "type": "EvidenceLine",
        "hasEvidenceItems": [
            {"type": "EvidenceLine", "directionOfEvidenceProvided": "neutral"}
        ],
        "directionOfEvidenceProvided": "supports",
    }
    el = EvidenceLine(**el_dict)
    assert isinstance(el.hasEvidenceItems[0], InformationEntity)
    assert el.hasEvidenceItems[0].type == "EvidenceLine"

    el_dict = {
        "type": "EvidenceLine",
        "hasEvidenceItems": ["evidence_items.json#/1"],
        "directionOfEvidenceProvided": "supports",
    }
    el = EvidenceLine(**el_dict)
    assert isinstance(el.hasEvidenceItems[0], iriReference)

    el_dict = {
        "type": "EvidenceLine",
        "hasEvidenceItems": None,
        "directionOfEvidenceProvided": "supports",
    }
    assert EvidenceLine(**el_dict)

    invalid_params = {
        "type": "EvidenceLine",
        "hasEvidenceItems": [Agent(name="Joe")],
        "directionOfEvidenceProvided": "supports",
    }
    with pytest.raises(ValueError, match="validation errors for EvidenceLine"):
        EvidenceLine(**invalid_params)

    invalid_params = {
        "type": "EvidenceLine",
        "hasEvidenceItems": [{"type": "Statement"}],
        "directionOfEvidenceProvided": "supports",
    }
    assert EvidenceLine(**invalid_params)


def test_variant_pathogenicity_stmt(pathogenicity_evidence_line_params):
    """Ensure VariantPathogenicityStatement model works as expected"""
    params = {
        "direction": "supports",
        "proposition": {
            "type": "VariantPathogenicityProposition",
            "predicate": "isCausalFor",
            "object": "conditions.json#/1",
            "subject": "alleles.json#/1",
        },
        "classification": {
            "primaryCoding": {"code": "pathogenic", "system": "ACMG Guidelines, 2015"}
        },
        "specifiedBy": {
            "reportedIn": {
                "type": "Document",
                "pmid": "25741868",
                "name": "ACMG Guidelines, 2015",
            }
        },
        "hasEvidenceLines": [pathogenicity_evidence_line_params],
    }
    statement = VariantPathogenicityStatement(**params)
    assert isinstance(statement.hasEvidenceLines[0], VariantPathogenicityEvidenceLine)

    invalid_params = deepcopy(params)
    del invalid_params["classification"]["primaryCoding"]
    invalid_params["classification"]["name"] = "test"
    with pytest.raises(ValueError, match="`primaryCoding` is required."):
        VariantPathogenicityStatement(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["classification"]["primaryCoding"]["system"] = (
        "AMP/ASCO/CAP Guidelines, 2017"
    )
    with pytest.raises(ValueError, match="`primaryCoding.system` must be one of"):
        VariantPathogenicityStatement(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["classification"]["primaryCoding"]["code"] = (
        "pathogenic, low penetrance"
    )
    with pytest.raises(ValueError, match="`primaryCoding.code` must be one of"):
        VariantPathogenicityStatement(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["classification"]["primaryCoding"]["system"] = (
        "ClinGen Low Penetrance and Risk Allele Recommendations, 2024"
    )
    invalid_params["classification"]["primaryCoding"]["code"] = "pathogenic"
    with pytest.raises(ValueError, match="`primaryCoding.code` must be one of"):
        VariantPathogenicityStatement(**invalid_params)

    invalid_params = deepcopy(params)
    del invalid_params["proposition"]  # proposition is required for statement
    with pytest.raises(ValueError, match="Field required"):
        VariantPathogenicityStatement(**invalid_params)


def test_statement_proposition_accepts_iri_reference():
    """Statements may reference a proposition instead of embedding one."""
    statement = Statement(proposition="propositions.json#/1")

    assert statement.proposition == iriReference(root="propositions.json#/1")


def test_base_statement_and_evidence_line_accept_generic_propositions():
    """Base models accept generic schema propositions."""
    proposition = Proposition(
        type="Proposition", subject={}, predicate="relatedTo", object={}
    )

    statement = Statement(proposition=proposition)
    evidence_line = EvidenceLine(
        directionOfEvidenceProvided="neutral", targetProposition=proposition
    )

    assert statement.proposition == proposition
    assert evidence_line.targetProposition == proposition


def test_concept_sets_accept_iri_references():
    """Concept sets accept schema-permitted IRIs."""
    condition_set = ConditionSet(
        concepts=["conditions.json#/1", "conditions.json#/2"],
        membershipOperator="OR",
    )
    therapy_group = TherapyGroup(
        concepts=["therapies.json#/1", "therapies.json#/2"],
        membershipOperator="AND",
    )

    assert all(isinstance(concept, iriReference) for concept in condition_set.concepts)
    assert all(isinstance(concept, iriReference) for concept in therapy_group.concepts)


def test_study_results_accept_iri_source_data_sets(caf):
    """Study result models accept IRI source datasets."""
    assert CohortAlleleFrequencyStudyResult(
        **(caf.model_dump() | {"sourceDataSet": "datasets.json#/1"})
    ).sourceDataSet == iriReference(root="datasets.json#/1")
    assert TumorVariantFrequencyStudyResult(
        focus="alleles.json#/1",
        affectedSampleCount=1,
        totalSampleCount=2,
        affectedFrequency=0.5,
        sourceDataSet="datasets.json#/1",
    ).sourceDataSet == iriReference(root="datasets.json#/1")
    assert ExperimentalVariantFunctionalImpactStudyResult(
        focus="alleles.json#/1", sourceDataSet="datasets.json#/1"
    ).sourceDataSet == iriReference(root="datasets.json#/1")


def test_variant_pathogenicity_el(pathogenicity_evidence_line_params):
    """Ensure VariantPathogenicityEvidenceLine model works as expected"""
    params = deepcopy(pathogenicity_evidence_line_params)
    vp = VariantPathogenicityEvidenceLine(**params)

    assert isinstance(vp.specifiedBy, Method)
    assert vp.evidenceOutcome == MappableConcept(
        primaryCoding=Coding(
            code=code(root="PS3_supporting"), system="ACMG Guidelines, 2015"
        ),
        name="ACMG 2015 PS3 Supporting Criterion Met",
    )

    invalid_params = deepcopy(params)
    invalid_params["evidenceOutcome"]["primaryCoding"]["code"] = "PS3 supporting"
    with pytest.raises(
        ValueError,
        match="`primaryCoding.code` does not match regex pattern",
    ):
        VariantPathogenicityEvidenceLine(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["strengthOfEvidenceProvided"] = None
    with pytest.raises(
        ValueError,
        match="`strengthOfEvidenceProvided` is required when `directionOfEvidenceProvided` is 'supports' or 'disputes'.",
    ):
        VariantPathogenicityEvidenceLine(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["strengthOfEvidenceProvided"]["primaryCoding"]["code"] = "definitive"
    with pytest.raises(ValueError, match="`primaryCoding.code` must be one of"):
        VariantPathogenicityEvidenceLine(**invalid_params)

    invalid_params = deepcopy(params)
    del invalid_params["specifiedBy"]["reportedIn"]
    with pytest.raises(ValueError, match="`specifiedBy.reportedIn` is required"):
        VariantPathogenicityEvidenceLine(**invalid_params)

    invalid_params = deepcopy(params)
    del invalid_params[
        "directionOfEvidenceProvided"
    ]  # directionOfEvidenceProvided is required for statement
    with pytest.raises(ValueError, match="Field required"):
        VariantPathogenicityEvidenceLine(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["strengthOfEvidenceProvided"] = {"name": "test"}
    with pytest.raises(ValueError, match="`primaryCoding` is required."):
        VariantPathogenicityEvidenceLine(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["strengthOfEvidenceProvided"] = {
        "primaryCoding": {
            "system": "AMP/ASCO/CAP Guidelines, 2017",
            "code": "strong",
        }
    }
    with pytest.raises(ValueError, match="`primaryCoding.system` must be"):
        VariantPathogenicityEvidenceLine(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["strengthOfEvidenceProvided"] = {
        "primaryCoding": {"system": "ACMG Guidelines, 2015", "code": "PS3"}
    }
    with pytest.raises(ValueError, match="`primaryCoding.code` must be"):
        VariantPathogenicityEvidenceLine(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["specifiedBy"]["methodType"] = "OS1"
    with pytest.raises(
        ValueError,
        match="'OS1' is not a valid VariantPathogenicityEvidenceLine.MethodType",
    ):
        VariantPathogenicityEvidenceLine(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["directionOfEvidenceProvided"] = "neutral"
    with pytest.raises(
        ValueError,
        match="`strengthOfEvidenceProvided` is not allowed when `directionOfEvidenceProvided` is 'neutral'.",
    ):
        VariantPathogenicityEvidenceLine(**invalid_params)


@pytest.mark.parametrize("outcome", ["no_criteria_met", "PS3_not_met"])
def test_pathogenicity_noncontributing_outcomes_require_neutral_without_strength(
    pathogenicity_evidence_line_params, outcome
):
    """Noncontributing ACMG outcomes must have neutral direction and no strength."""
    params = deepcopy(pathogenicity_evidence_line_params)
    strength = deepcopy(params["strengthOfEvidenceProvided"])
    params["evidenceOutcome"]["primaryCoding"]["code"] = outcome
    params["directionOfEvidenceProvided"] = "neutral"
    params["strengthOfEvidenceProvided"] = None
    assert VariantPathogenicityEvidenceLine(**params)

    invalid_direction = deepcopy(params)
    invalid_direction["directionOfEvidenceProvided"] = "supports"
    invalid_direction["strengthOfEvidenceProvided"] = strength
    with pytest.raises(
        ValueError, match="`directionOfEvidenceProvided` must be 'neutral'"
    ):
        VariantPathogenicityEvidenceLine(**invalid_direction)

    invalid_strength = deepcopy(params)
    invalid_strength["strengthOfEvidenceProvided"] = strength
    with pytest.raises(ValueError, match="`strengthOfEvidenceProvided` must be null"):
        VariantPathogenicityEvidenceLine(**invalid_strength)


def test_pathogenicity_profile_accepts_schema_permitted_references():
    """Pathogenicity models accept opaque IRI references."""
    evidence_line = VariantPathogenicityEvidenceLine(
        specifiedBy="methods.json#/1",
        directionOfEvidenceProvided="supports",
        evidenceOutcome="outcomes.json#/1",
        strengthOfEvidenceProvided="strengths.json#/1",
    )
    statement = VariantPathogenicityStatement(
        proposition="propositions.json#/1",
        strength="strengths.json#/1",
        classification="classifications.json#/1",
        specifiedBy="methods.json#/1",
    )

    assert isinstance(evidence_line.evidenceOutcome, iriReference)
    assert isinstance(statement.classification, iriReference)


def test_variant_onco_stmt(oncogenicity_evidence_line_params):
    """Ensure VariantOncogenicityStatement model works as expected"""
    params = {
        "direction": "neutral",
        "proposition": {
            "type": "VariantOncogenicityProposition",
            "predicate": "isOncogenicFor",
            "object": "conditions.json#/1",
            "subject": "alleles.json#/1",
        },
        "classification": {
            "primaryCoding": {
                "code": "oncogenic",
                "system": "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
            }
        },
        "specifiedBy": "documents.json#/1",
        "strength": {
            "primaryCoding": {
                "code": "definitive",
                "system": "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
            }
        },
        "hasEvidenceLines": [oncogenicity_evidence_line_params],
    }
    statement = VariantOncogenicityStatement(**params)
    assert isinstance(statement.hasEvidenceLines[0], VariantOncogenicityEvidenceLine)

    valid_params = deepcopy(params)
    valid_params["strength"] = None
    assert VariantOncogenicityStatement(**valid_params)

    invalid_params = deepcopy(params)
    invalid_params["strength"]["primaryCoding"]["code"] = "oncogenic"
    with pytest.raises(ValueError, match="`primaryCoding.code` must be one of"):
        VariantOncogenicityStatement(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["strength"]["primaryCoding"]["system"] = "ACMG Guidelines, 2015"
    with pytest.raises(ValueError, match="`primaryCoding.system` must be"):
        VariantOncogenicityStatement(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["classification"]["primaryCoding"]["code"] = "pathogenic"
    with pytest.raises(ValueError, match="`primaryCoding.code` must be one of"):
        VariantOncogenicityStatement(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["classification"]["primaryCoding"]["system"] = (
        "ACMG Guidelines, 2015"
    )
    with pytest.raises(ValueError, match="`primaryCoding.system` must be"):
        VariantOncogenicityStatement(**invalid_params)


def test_variant_onco_el(oncogenicity_evidence_line_params):
    """Ensure VariantOncogenicityEvidenceLine model works as expected"""
    vo = VariantOncogenicityEvidenceLine(**oncogenicity_evidence_line_params)
    assert isinstance(vo.specifiedBy, Method)
    assert vo.evidenceOutcome == MappableConcept(
        primaryCoding=Coding(
            code=code(root="OS2_supporting"),
            system="ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
        ),
    )

    vo_invalid_params = vo.model_copy(deep=True).model_dump()
    vo_invalid_params["specifiedBy"]["methodType"] = "PS1"
    with pytest.raises(
        ValueError,
        match="'PS1' is not a valid VariantOncogenicityEvidenceLine.MethodType",
    ):
        VariantOncogenicityEvidenceLine(**vo_invalid_params)

    invalid_params = vo.model_copy(deep=True).model_dump()
    invalid_params["strengthOfEvidenceProvided"]["primaryCoding"]["code"] = "definitive"
    with pytest.raises(ValueError, match="`primaryCoding.code` must be one of"):
        VariantOncogenicityEvidenceLine(**invalid_params)

    invalid_params = vo.model_copy(deep=True).model_dump()
    invalid_params["strengthOfEvidenceProvided"]["primaryCoding"]["system"] = (
        "ACMG Guidelines, 2015"
    )
    with pytest.raises(
        ValueError,
        match="`primaryCoding.system` must be 'ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022'.",
    ):
        VariantOncogenicityEvidenceLine(**invalid_params)

    invalid_params = vo.model_copy(deep=True).model_dump()
    invalid_params["directionOfEvidenceProvided"] = "neutral"
    with pytest.raises(
        ValueError,
        match="`strengthOfEvidenceProvided` is not allowed when `directionOfEvidenceProvided` is 'neutral'.",
    ):
        VariantOncogenicityEvidenceLine(**invalid_params)


@pytest.mark.parametrize("outcome", ["no_criteria_met", "OS2_not_met"])
def test_oncogenicity_noncontributing_outcomes_require_neutral_without_strength(
    oncogenicity_evidence_line_params, outcome
):
    """Noncontributing CCV outcomes must have neutral direction and no strength."""
    params = deepcopy(oncogenicity_evidence_line_params)
    strength = deepcopy(params["strengthOfEvidenceProvided"])
    params["evidenceOutcome"]["primaryCoding"]["code"] = outcome
    params["directionOfEvidenceProvided"] = "neutral"
    params["strengthOfEvidenceProvided"] = None
    assert VariantOncogenicityEvidenceLine(**params)

    invalid_direction = deepcopy(params)
    invalid_direction["directionOfEvidenceProvided"] = "supports"
    invalid_direction["strengthOfEvidenceProvided"] = strength
    with pytest.raises(
        ValueError, match="`directionOfEvidenceProvided` must be 'neutral'"
    ):
        VariantOncogenicityEvidenceLine(**invalid_direction)

    invalid_strength = deepcopy(params)
    invalid_strength["strengthOfEvidenceProvided"] = strength
    with pytest.raises(ValueError, match="`strengthOfEvidenceProvided` must be null"):
        VariantOncogenicityEvidenceLine(**invalid_strength)


def test_oncogenicity_profile_accepts_schema_permitted_references():
    """Oncogenicity models accept inherited IRI branches."""
    evidence_line = VariantOncogenicityEvidenceLine(
        specifiedBy="methods.json#/1",
        directionOfEvidenceProvided="supports",
        evidenceOutcome="outcomes.json#/1",
        strengthOfEvidenceProvided="strengths.json#/1",
    )
    statement = VariantOncogenicityStatement(
        proposition="propositions.json#/1",
        strength="strengths.json#/1",
        classification="classifications.json#/1",
        specifiedBy="methods.json#/1",
    )

    assert isinstance(evidence_line.evidenceOutcome, iriReference)
    assert isinstance(statement.classification, iriReference)


def test_variant_onco_el_no_evidence_outcome():
    """Test that VariantOncogenicityEvidenceLine validates without evidence
    outcome
    """
    valid = VariantOncogenicityEvidenceLine(
        type="EvidenceLine",
        specifiedBy={
            "type": "Method",
            "reportedIn": {
                "type": "Document",
                "pmid": "35101336",
                "name": "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
            },
            "methodType": "functional_data_assessment",
        },
        directionOfEvidenceProvided=Direction.NEUTRAL,
        scoreOfEvidenceProvided=0,
        evidenceOutcome=None,
    )

    assert valid

    invalid = valid.model_dump()
    invalid["specifiedBy"]["methodType"] = "dummy"

    with pytest.raises(
        ValueError,
        match="'dummy' is not a valid VariantOncogenicityEvidenceLine.MethodType",
    ):
        VariantOncogenicityEvidenceLine.model_validate(invalid)


def test_aac_profile_accepts_schema_permitted_references():
    """AAC models accept opaque classification and strength IRIs."""
    statement = VariantClinicalSignificanceStatement(
        proposition="propositions.json#/1",
        strength="strengths.json#/1",
        classification="classifications.json#/1",
        specifiedBy="methods.json#/1",
    )

    assert isinstance(statement.strength, iriReference)
    assert isinstance(statement.classification, iriReference)


def test_aac_statement():
    """Test that AMP/ASCO/CAP statement model validators work correctly"""
    prop = {
        "type": "VariantDiagnosticProposition",
        "predicate": "isDiagnosticExclusionCriterionFor",
        "object": "conditions.json#/1",
        "subject": "alleles.json#/1",
    }
    params = {
        "direction": "supports",
        "proposition": {
            "type": "VariantClinicalSignificanceProposition",
            "predicate": "hasClinicalSignificanceFor",
            "object": "conditions.json#/1",
            "subject": "alleles.json#/1",
        },
        "strength": {
            "primaryCoding": {
                "code": "strong",
                "system": "AMP/ASCO/CAP Guidelines, 2017",
            }
        },
        "specifiedBy": "documents.json#/1",
        "classification": {
            "name": "Tier I",
            "primaryCoding": {
                "code": "tier i",
                "system": "AMP/ASCO/CAP Guidelines, 2017",
            },
        },
        "hasEvidenceLines": [
            "evidence_lines.json#/1",  # iri
            {
                "targetProposition": prop,
                "directionOfEvidenceProvided": "supports",
                "strengthOfEvidenceProvided": {
                    "primaryCoding": {
                        "code": "A",
                        "system": "AMP/ASCO/CAP Guidelines, 2017",
                    }
                },
                "hasEvidenceItems": [
                    "evidence_items.json#/1",
                    {
                        "type": "Statement",
                        "direction": "supports",
                        "proposition": prop,
                        "strength": {
                            "primaryCoding": {
                                "code": "A",
                                "system": "System",
                            }
                        },
                        "specifiedBy": "documents.json#/1",
                    },
                ],
            },
        ],
    }
    assert VariantClinicalSignificanceStatement(**params)

    # No strengthOfEvidenceProvided
    no_evidence_line_strength_params = deepcopy(params)
    no_evidence_line_strength_params["hasEvidenceLines"][1].pop(
        "strengthOfEvidenceProvided"
    )
    assert VariantClinicalSignificanceStatement(**no_evidence_line_strength_params)

    # Invalid strength
    invalid_params = deepcopy(params)
    invalid_params["strength"]["primaryCoding"]["code"] = "Strong"
    with pytest.raises(ValidationError, match="`strength` must be: strong"):
        VariantClinicalSignificanceStatement(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["strength"]["primaryCoding"]["code"] = "potential"
    with pytest.raises(ValidationError, match="`strength` must be: strong"):
        VariantClinicalSignificanceStatement(**invalid_params)

    # Invalid classification
    invalid_params = deepcopy(params)
    invalid_params["classification"]["primaryCoding"]["code"] = "Tier I"
    with pytest.raises(ValidationError, match="`primaryCoding.code` must be one of"):
        VariantClinicalSignificanceStatement(**invalid_params)

    invalid_params = deepcopy(params)
    invalid_params["classification"]["name"] = "tier i"
    with pytest.raises(ValidationError, match="`classification.name` must be: Tier I"):
        VariantClinicalSignificanceStatement(**invalid_params)

    # Invalid direction
    invalid_params = deepcopy(params)
    invalid_params["direction"] = "disputes"
    with pytest.raises(ValidationError, match="`direction` must be: supports"):
        VariantClinicalSignificanceStatement(**invalid_params)

    # Invalid targetProposition
    invalid_params = deepcopy(params)
    invalid_params["hasEvidenceLines"][1]["targetProposition"] = invalid_params[
        "proposition"
    ]
    with pytest.raises(ValidationError, match="`hasEvidenceLines` must be one of"):
        VariantClinicalSignificanceStatement(**invalid_params)


def test_examples(test_definitions):
    """Test VA Spec examples"""
    va_spec_schema_mapping = {
        "va-spec.base": base,
        "va-spec.acmg-2015": acmg_2015,
        "va-spec.ccv-2022": ccv_2022,
    }

    for test in test_definitions["tests"]:
        with (VA_SPEC_TEST_FIXTURES / test["test_file"]).open() as f:
            data = yaml.safe_load(f)

        ns = test["namespace"]
        pydantic_models = va_spec_schema_mapping.get(ns)
        if not pydantic_models:
            continue

        schema_model = test["definition"]
        if schema_model == "Statement":
            continue

        pydantic_model = getattr(pydantic_models, schema_model, False)
        assert pydantic_model, schema_model

        try:
            assert pydantic_model(**data)
        except ValidationError as e:
            err_msg = f"ValidationError in {test['test_file']}: {e}"
            raise AssertionError(err_msg)  # noqa: B904
