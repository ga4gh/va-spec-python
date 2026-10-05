"""Regression tests for public package imports."""

import subprocess
import sys


def test_public_modules_import_and_resolve_recursive_models():
    """Import public modules and construct recursive models in a clean process."""
    script = """
import ga4gh.va_spec
import ga4gh.va_spec.aac_2017
import ga4gh.va_spec.acmg_2015
import ga4gh.va_spec.base
import ga4gh.va_spec.ccv_2022
from ga4gh.va_spec.base import Direction, Statement

Statement(
    direction=Direction.SUPPORTS,
    proposition={"type": "Proposition", "subject": {}, "predicate": "relatedTo", "object": {}},
    hasEvidence=[
        {
            "type": "Statement",
            "direction": "supports",
            "proposition": {"type": "Proposition", "subject": {}, "predicate": "relatedTo", "object": {}},
        }
    ],
)
"""
    result = subprocess.run(
        [sys.executable, "-c", script],  # noqa: S603  # Controlled test process.
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
