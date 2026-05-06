"""Test that CCV 2022 derived evidence is working correctly"""

import pytest

from ga4gh.va_spec.ccv_2022 import (
    VariantOncogenicityEvidenceLine,
    derive_onco_evidence_attributes,
)


@pytest.mark.parametrize(
    ("criterion", "expected_strength", "expected_score"),
    [
        (
            VariantOncogenicityEvidenceLine.Criterion.OP1,
            "supporting",
            1,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OP2,
            "supporting",
            1,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OP3,
            "supporting",
            1,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OP4,
            "supporting",
            1,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OM1,
            "moderate",
            2,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OM2,
            "moderate",
            2,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OM3,
            "moderate",
            2,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OM4,
            "moderate",
            2,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OS1,
            "strong",
            4,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OS2,
            "strong",
            4,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OS3,
            "strong",
            4,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.OVS1,
            "very strong",
            8,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBP1,
            "supporting",
            -1,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBP2,
            "supporting",
            -1,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBS1,
            "strong",
            -4,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBS2,
            "strong",
            -4,
        ),
        (
            VariantOncogenicityEvidenceLine.Criterion.SBVS1,
            "very strong",
            -8,
        ),
    ],
)
def test_derive_onco_evidence_attributes(
    criterion,
    expected_strength,
    expected_score,
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
