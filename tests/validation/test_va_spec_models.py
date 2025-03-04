"""Test VA Spec Pydantic model"""

import json

import pytest
from ga4gh.core.models import iriReference
from ga4gh.va_spec.aac_2017.models import VariantTherapeuticResponseStudyStatement
from ga4gh.va_spec.base import (
    Agent,
    CohortAlleleFrequencyStudyResult,
    ExperimentalVariantFunctionalImpactStudyResult,
)
from ga4gh.va_spec.base.core import EvidenceLine, StudyGroup, StudyResult
from pydantic import ValidationError


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
