"""Test VA Spec Pydantic model"""

import json

import pytest
import yaml
from ga4gh.core.models import Coding, MappableConcept, code, iriReference
from ga4gh.va_spec import acmg_2015, base, ccv_2022
from ga4gh.va_spec.aac_2017.models import VariantTherapeuticResponseStudyStatement
from ga4gh.va_spec.acmg_2015.models import (
    VariantPathogenicityFunctionalImpactEvidenceLine,
)
from ga4gh.va_spec.base import (
    Agent,
    CohortAlleleFrequencyStudyResult,
    ExperimentalVariantFunctionalImpactStudyResult,
)
from ga4gh.va_spec.base.core import EvidenceLine, StudyGroup, StudyResult
from ga4gh.va_spec.ccv_2022.models import (
    VariantOncogenicityFunctionalImpactEvidenceLine,
)
from pydantic import ValidationError

from tests.conftest import SUBMODULES_DIR

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
        focusAllele="allele.json#/1",
        focusAlleleCount=0,
        focusAlleleFrequency=0,
        locusAlleleCount=34086,
        cohort=StudyGroup(id="ALL", name="Overall"),
    )


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
    assert caf.focusAllele.root == "allele.json#/1"
    assert caf.focusAlleleCount == 0
    assert caf.focusAlleleFrequency == 0
    assert caf.locusAlleleCount == 34086
    assert caf.cohort.id == "ALL"
    assert caf.cohort.name == "Overall"
    assert caf.cohort.type == "StudyGroup"

    assert "focus" not in caf.model_dump()
    assert "focus" not in json.loads(caf.model_dump_json())

    with pytest.raises(
        AttributeError,
        match="'CohortAlleleFrequencyStudyResult' object has no attribute 'focus'",
    ):
        caf.focus  # noqa: B018

    with pytest.raises(
        ValueError,
        match='"CohortAlleleFrequencyStudyResult" object has no field "focus"',
    ):
        caf.focus = "focus"


def test_experimental_func_impact_study_result():
    """Ensure ExperimentalVariantFunctionalImpactStudyResult model works as expected"""
    experimental_func_impact_study_result = (
        ExperimentalVariantFunctionalImpactStudyResult(focusVariant="allele.json#/1")
    )
    assert experimental_func_impact_study_result.focusVariant.root == "allele.json#/1"

    assert "focus" not in experimental_func_impact_study_result.model_dump()
    assert "focus" not in json.loads(
        experimental_func_impact_study_result.model_dump_json()
    )

    with pytest.raises(
        AttributeError,
        match="'ExperimentalVariantFunctionalImpactStudyResult' object has no attribute 'focus'",
    ):
        experimental_func_impact_study_result.focus  # noqa: B018

    with pytest.raises(
        ValueError,
        match='"ExperimentalVariantFunctionalImpactStudyResult" object has no field "focus"',
    ):
        experimental_func_impact_study_result.focus = "focus"


def test_evidence_line(caf):
    """Ensure EvidenceLine model works as expected"""
    el_dict = {
        "type": "EvidenceLine",
        "hasEvidenceItems": [
            {
                "id": "civic.eid:2997",
                "type": "Statement",
                "proposition": {
                    "type": "VariantTherapeuticResponseProposition",
                    "subjectVariant": {
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
                    "objectTherapeutic": {
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
                        "system": "AMP/ASCO/CAP (AAC) Guidelines, 2017",
                        "code": "Level A",
                    }
                },
                "classification": {
                    "primaryCoding": {
                        "system": "AMP/ASCO/CAP (AAC) Guidelines, 2017",
                        "code": "Tier I",
                    }
                },
                "specifiedBy": {
                    "id": "civic.method:2019",
                    "name": "CIViC Curation SOP (2019)",
                    "reportedIn": {
                        "name": "Danos et al., 2019, Genome Med.",
                        "title": "Standard operating procedure for curation and clinical interpretation of variants in cancer",
                        "doi": "10.1186/s13073-019-0687-x",
                        "pmid": 31779674,
                        "type": "Document",
                    },
                    "type": "Method",
                },
                "direction": "supports",
            }
        ],
        "directionOfEvidenceProvided": "disputes",
    }
    el = EvidenceLine(**el_dict)
    assert isinstance(el.hasEvidenceItems[0], VariantTherapeuticResponseStudyStatement)

    el_dict = {
        "type": "EvidenceLine",
        "hasEvidenceItems": [caf.model_dump(exclude_none=True)],
        "directionOfEvidenceProvided": "supports",
    }
    el = EvidenceLine(**el_dict)
    assert isinstance(el.hasEvidenceItems[0], StudyResult)
    assert isinstance(el.hasEvidenceItems[0].root, CohortAlleleFrequencyStudyResult)

    el_dict = {
        "type": "EvidenceLine",
        "hasEvidenceItems": [
            {"type": "EvidenceLine", "directionOfEvidenceProvided": "neutral"}
        ],
        "directionOfEvidenceProvided": "supports",
    }
    el = EvidenceLine(**el_dict)
    assert isinstance(el.hasEvidenceItems[0], EvidenceLine)

    el_dict = {
        "type": "EvidenceLine",
        "hasEvidenceItems": ["evidence_items.json#/1"],
        "directionOfEvidenceProvided": "supports",
    }
    el = EvidenceLine(**el_dict)
    assert isinstance(el.hasEvidenceItems[0], iriReference)


def test_variant_pathogenicity_el():
    """Ensure VariantPathogenicityFunctionalImpactEvidenceLine model works as expected"""
    vp = VariantPathogenicityFunctionalImpactEvidenceLine(
        type="EvidenceLine",
        specifiedBy={
            "type": "Method",
            "id": "PS3",
            "name": "ACMG 2015 PS3 Criterion",
            "reportedIn": {
                "type": "Document",
                "pmid": 25741868,
                "name": "ACMG Guidelines, 2015",
            },
        },
        directionOfEvidenceProvided="supports",
        evidenceOutcome={
            "primaryCoding": {
                "code": "PS3_supporting",
                "system": "ACMG Guidelines, 2015",
            },
            "name": "ACMG 2015 PS3 Supporting Criterion Met",
        },
    )
    assert vp.evidenceOutcome == MappableConcept(
        primaryCoding=Coding(
            code=code(root="PS3_supporting"), system="ACMG Guidelines, 2015"
        ),
        name="ACMG 2015 PS3 Supporting Criterion Met",
    )


def test_variant_onco_el():
    """Ensure VariantOncogenicityFunctionalImpactEvidenceLine model works as expected"""
    vo = VariantOncogenicityFunctionalImpactEvidenceLine(
        type="EvidenceLine",
        specifiedBy={
            "type": "Method",
            "reportedIn": {
                "type": "Document",
                "pmid": 35101336,
                "name": "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
            },
        },
        directionOfEvidenceProvided="supports",
        scoreOfEvidenceProvided=1,
        evidenceOutcome={
            "primaryCoding": {
                "code": "OS2_supporting",
                "system": "ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
            },
        },
    )
    assert vo.evidenceOutcome == MappableConcept(
        primaryCoding=Coding(
            code=code(root="OS2_supporting"),
            system="ClinGen/CGC/VICC Guidelines for Oncogenicity, 2022",
        ),
    )


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
