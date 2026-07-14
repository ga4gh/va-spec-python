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
    assert onco_evidence_attrs.methodType == expected_method_type
