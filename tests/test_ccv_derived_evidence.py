"""Test that CCV 2022 derived evidence is working correctly"""

import pytest

from ga4gh.va_spec.ccv_2022 import (
    VariantOncogenicityEvidenceLine,
    derive_onco_evidence_attributes,
)


@pytest.mark.parametrize(
    ("criterion", "expected_strength", "expected_score", "expected_method_type"),
    [
        (
            VariantOncogenicityEvidenceLine.Criterion.OP1,
            "supporting",
            1,
            VariantOncogenicityEvidenceLine.MethodType.COMPUTATIONAL_PREDICTION,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OP2,
            "supporting",
            1,
            VariantOncogenicityEvidenceLine.MethodType.SINGLE_GENETIC_ETIOLOGY_CONTEXT,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OP3,
            "supporting",
            1,
            VariantOncogenicityEvidenceLine.MethodType.SOMATIC_HOTSPOT_RECURRENCE,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OP4,
            "supporting",
            1,
            VariantOncogenicityEvidenceLine.MethodType.POPULATION_FREQUENCY,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OM1,
            "moderate",
            2,
            VariantOncogenicityEvidenceLine.MethodType.FUNCTIONAL_DOMAIN_LOCATION,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OM2,
            "moderate",
            2,
            VariantOncogenicityEvidenceLine.MethodType.PRIMARY_SEQUENCE_CONSEQUENCE,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OM3,
            "moderate",
            2,
            VariantOncogenicityEvidenceLine.MethodType.SOMATIC_HOTSPOT_RECURRENCE,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OM4,
            "moderate",
            2,
            VariantOncogenicityEvidenceLine.MethodType.AMINO_ACID_OR_RESIDUE_ANALOGY,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OS1,
            "strong",
            4,
            VariantOncogenicityEvidenceLine.MethodType.AMINO_ACID_OR_RESIDUE_ANALOGY,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OS2,
            "strong",
            4,
            VariantOncogenicityEvidenceLine.MethodType.FUNCTIONAL_ASSAY,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OS3,
            "strong",
            4,
            VariantOncogenicityEvidenceLine.MethodType.SOMATIC_HOTSPOT_RECURRENCE,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OVS1,
            "very strong",
            8,
            VariantOncogenicityEvidenceLine.MethodType.PRIMARY_SEQUENCE_CONSEQUENCE,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBP1,
            "supporting",
            -1,
            VariantOncogenicityEvidenceLine.MethodType.COMPUTATIONAL_PREDICTION,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBP2,
            "supporting",
            -1,
            VariantOncogenicityEvidenceLine.MethodType.PRIMARY_SEQUENCE_CONSEQUENCE,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBS1,
            "strong",
            -4,
            VariantOncogenicityEvidenceLine.MethodType.POPULATION_FREQUENCY,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBS2,
            "strong",
            -4,
            VariantOncogenicityEvidenceLine.MethodType.FUNCTIONAL_ASSAY,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBVS1,
            "very strong",
            -8,
            VariantOncogenicityEvidenceLine.MethodType.POPULATION_FREQUENCY,
        ),
    ],
)
def test_derive_onco_evidence_attributes(
    criterion, expected_strength, expected_score, expected_method_type
):
    """Test that derive_onco_evidence_attributes works correctly"""
    onco_evidence_attrs = derive_onco_evidence_attributes(criterion)

    assert (
        onco_evidence_attrs.evidenceOutcome.primaryCoding.code.root == criterion.value
    )
    assert (
        onco_evidence_attrs.strengthOfEvidenceProvided.primaryCoding.code.root
        == expected_strength
    )
    assert onco_evidence_attrs.scoreOfEvidenceProvided == expected_score
    expected_direction = "disputes" if expected_score < 0 else "supports"
    assert onco_evidence_attrs.directionOfEvidenceProvided == expected_direction
    assert onco_evidence_attrs.specifiedBy.methodType == expected_method_type.value


@pytest.mark.parametrize(
    ("outcome", "expected_direction", "expected_score", "expected_method_type"),
    [
        (
            "OS2_moderate",
            "supports",
            2,
            VariantOncogenicityEvidenceLine.MethodType.FUNCTIONAL_ASSAY,
        ),
        (
            "SBS2_moderate",
            "disputes",
            -2,
            VariantOncogenicityEvidenceLine.MethodType.FUNCTIONAL_ASSAY,
        ),
    ],
)
def test_derive_onco_evidence_attributes_with_adjusted_strength(
    outcome, expected_direction, expected_score, expected_method_type
):
    """Test that the outcome's adjusted strength determines strength and score."""
    onco_evidence_attrs = derive_onco_evidence_attributes(outcome)

    evidence_outcome = onco_evidence_attrs.evidenceOutcome.primaryCoding.code.root
    assert evidence_outcome == outcome
    evidence_line = VariantOncogenicityEvidenceLine(**onco_evidence_attrs.model_dump())
    assert evidence_line.evidenceOutcome.primaryCoding.code.root == evidence_outcome
    assert onco_evidence_attrs.directionOfEvidenceProvided == expected_direction
    assert (
        onco_evidence_attrs.strengthOfEvidenceProvided.primaryCoding.code.root
        == "moderate"
    )
    assert onco_evidence_attrs.scoreOfEvidenceProvided == expected_score
    assert onco_evidence_attrs.specifiedBy.methodType == expected_method_type.value


@pytest.mark.parametrize(
    ("provided_outcome", "expected_outcome"),
    [
        ("OS2_MODERATE", "OS2_moderate"),
        ("OS2_Moderate", "OS2_moderate"),
        ("OS2_NOT_MET", "OS2_not_met"),
    ],
)
def test_derive_onco_evidence_attributes_normalizes_modifier(
    provided_outcome, expected_outcome
):
    """Test that outcome modifiers are normalized to lowercase."""
    onco_evidence_attrs = derive_onco_evidence_attributes(provided_outcome)

    assert (
        onco_evidence_attrs.evidenceOutcome.primaryCoding.code.root == expected_outcome
    )


def test_derive_onco_evidence_attributes_does_not_normalize_criterion():
    """Test that criterion codes must retain their canonical uppercase form."""
    with pytest.raises(ValueError, match="Invalid CCV evidence outcome"):
        derive_onco_evidence_attributes("os2_MODERATE")


def test_derive_onco_evidence_attributes_from_not_met_outcome():
    """Test that a not-met outcome has no strength or score."""
    onco_evidence_attrs = derive_onco_evidence_attributes("OS2_not_met")

    assert onco_evidence_attrs.evidenceOutcome.primaryCoding.code.root == "OS2_not_met"
    assert onco_evidence_attrs.directionOfEvidenceProvided == "neutral"
    assert onco_evidence_attrs.strengthOfEvidenceProvided is None
    assert onco_evidence_attrs.scoreOfEvidenceProvided is None
    assert (
        onco_evidence_attrs.specifiedBy.methodType
        == VariantOncogenicityEvidenceLine.MethodType.FUNCTIONAL_ASSAY.value
    )
    VariantOncogenicityEvidenceLine(**onco_evidence_attrs.model_dump())
