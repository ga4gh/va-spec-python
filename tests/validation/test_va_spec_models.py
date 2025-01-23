"""Test VA Spec Pydantic model"""

import pytest
from ga4gh.va_spec.base import (
    Agent,
    CohortAlleleFrequencyStudyResult,
    ExperimentalVariantFunctionalImpactStudyResult,
)
from ga4gh.va_spec.base.core import StudyGroup


def test_agent():
    """Ensure Agent model works as expected

    Tests that extends property is implemented correctly in the Pydantic models
    """
    assert "label" not in Agent.model_fields

    agent = Agent(name="Joe")
    assert agent.type == "Agent"
    assert agent.name == "Joe"

    with pytest.raises(AttributeError, match="'Agent' object has no attribute 'label'"):
        agent.label  # noqa: B018

    with pytest.raises(ValueError, match='"Agent" object has no field "label"'):
        agent.label = "This is an agent"


def test_caf_study_result():
    """Ensure CohortAlleleFrequencyStudyResult model works as expected

    Tests that extends property is implemented correctly in the Pydantic models
    """
    assert "focus" not in CohortAlleleFrequencyStudyResult.model_fields

    caf = CohortAlleleFrequencyStudyResult(
        focusAllele="allele.json#/1",
        focusAlleleCount=0,
        focusAlleleFrequency=0,
        locusAlleleCount=34086,
        cohort=StudyGroup(id="ALL", label="Overall"),
    )
    assert caf.focusAllele.root == "allele.json#/1"
    assert caf.focusAlleleCount == 0
    assert caf.focusAlleleFrequency == 0
    assert caf.locusAlleleCount == 34086
    assert caf.cohort.id == "ALL"
    assert caf.cohort.label == "Overall"
    assert caf.cohort.type == "StudyGroup"

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
    """Ensure ExperimentalVariantFunctionalImpactStudyResult model works as expected

    Tests that extends property is implemented correctly in the Pydantic models
    """
    assert "focus" not in ExperimentalVariantFunctionalImpactStudyResult.model_fields

    experimental_func_impact_study_result = (
        ExperimentalVariantFunctionalImpactStudyResult(focusVariant="allele.json#/1")
    )
    assert experimental_func_impact_study_result.focusVariant.root == "allele.json#/1"

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
