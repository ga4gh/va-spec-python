"""Test model metadata against the VA-Spec source and JSON schemas."""

import json
from pathlib import Path

import pytest
import yaml

from ga4gh.core.metadata import Maturity
from ga4gh.va_spec import VASPEC_VERSION, base
from ga4gh.va_spec.aac_2017 import models as aac_2017
from ga4gh.va_spec.acmg_2015 import models as acmg_2015
from ga4gh.va_spec.ccv_2022 import models as ccv_2022

SCHEMA_DIR = Path(__file__).parents[2] / "submodules" / "va_spec" / "schema" / "va-spec"
SCHEMAS = (
    (base, "base", SCHEMA_DIR / "base" / "va-core-source.yaml"),
    (base, "base", SCHEMA_DIR / "base" / "domain-entities-source.yaml"),
    (aac_2017, "aac-2017", SCHEMA_DIR / "aac-2017" / "profile-source.yaml"),
    (acmg_2015, "acmg-2015", SCHEMA_DIR / "acmg-2015" / "profile-source.yaml"),
    (ccv_2022, "ccv-2022", SCHEMA_DIR / "ccv-2022" / "profile-source.yaml"),
)


def _model_params():
    """Return model metadata discovered from all VA-Spec source YAML files."""
    params = []
    for model_module, namespace, source_path in SCHEMAS:
        with source_path.open() as source_file:
            definitions = yaml.safe_load(source_file)["$defs"]
        for name, definition in definitions.items():
            schema_path = SCHEMA_DIR / namespace / "json" / name
            if not schema_path.exists():
                continue
            model = getattr(model_module, name)
            with schema_path.open() as schema_file:
                schema = json.load(schema_file)
            params.append(pytest.param(model, namespace, definition, schema, id=name))
    assert params, "No concrete VA-Spec models discovered"
    return params


def test_va_spec_version_matches_source_schema():
    """The package version matches the authoritative VA-Spec source schema."""
    with SCHEMAS[0][2].open() as source_file:
        source_id = yaml.safe_load(source_file)["$id"]
    source_version = source_id.split("/va-spec/", maxsplit=1)[1].split("/", maxsplit=1)[
        0
    ]
    assert source_version == VASPEC_VERSION


@pytest.mark.parametrize(
    ("model", "namespace", "definition", "schema"), _model_params()
)
def test_model_metadata(model, namespace, definition, schema):
    """Model metadata matches its source and generated JSON Schemas."""
    expected_schema_id = (
        f"https://w3id.org/ga4gh/schema/va-spec/{VASPEC_VERSION}/{namespace}/json/"
        f"{model.__name__}"
    )
    assert model.schema_id() == expected_schema_id
    assert "_maturity" in model.__dict__
    assert model.maturity() == Maturity(definition["maturity"])

    generated_schema = model.model_json_schema()
    assert generated_schema["$id"] == expected_schema_id
    assert generated_schema["maturity"] == schema["maturity"]
    assert "ga4gh" not in generated_schema
