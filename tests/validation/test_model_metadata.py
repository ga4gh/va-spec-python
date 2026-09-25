"""Test model metadata against the VA-Spec source and JSON schemas."""

import json
from pathlib import Path

import pytest

from ga4gh.core.metadata import Maturity
from ga4gh.va_spec import VASPEC_VERSION, base
from ga4gh.va_spec.aac_2017 import models as aac_2017
from ga4gh.va_spec.acmg_2015 import models as acmg_2015
from ga4gh.va_spec.ccv_2022 import models as ccv_2022

SCHEMA_DIR = Path(__file__).parents[2] / "submodules" / "va_spec" / "schema" / "va-spec"
JSON_DIR = SCHEMA_DIR / "json"
SCHEMA_MODULES = {
    "": base,
    "aac-2017": aac_2017,
    "acmg-2015": acmg_2015,
    "ccv-2022": ccv_2022,
}


def _model_params():
    """Return model metadata discovered from VA-Spec JSON Schemas."""
    params = []
    for schema_path in JSON_DIR.rglob("*"):
        if not schema_path.is_file():
            continue
        with schema_path.open() as schema_file:
            schema = json.load(schema_file)
        namespace = str(schema_path.parent.relative_to(JSON_DIR))
        namespace = "" if namespace == "." else namespace
        model_module = SCHEMA_MODULES.get(namespace)
        if model_module is None:
            continue
        model = getattr(model_module, schema["title"])
        params.append(pytest.param(model, schema, id=schema["title"]))
    assert params, "No concrete VA-Spec models discovered"
    return params


def test_va_spec_version_matches_json_schemas():
    """The package version matches every VA-Spec JSON Schema identifier."""
    for schema_path in JSON_DIR.rglob("*"):
        if not schema_path.is_file():
            continue
        with schema_path.open() as schema_file:
            schema_id = json.load(schema_file)["$id"]
        source_version = schema_id.split("/va-spec/", maxsplit=1)[1].split(
            "/", maxsplit=1
        )[0]
        assert source_version == VASPEC_VERSION


@pytest.mark.parametrize(("model", "schema"), _model_params())
def test_model_metadata(model, schema):
    """Model metadata matches its generated JSON Schema."""
    expected_schema_id = schema["$id"]
    assert model.schema_id() == expected_schema_id
    assert "_maturity" in model.__dict__
    assert model.maturity() == Maturity(schema["maturity"])

    generated_schema = model.model_json_schema()
    assert generated_schema["$id"] == expected_schema_id
    assert generated_schema["maturity"] == schema["maturity"]
    assert "ga4gh" not in generated_schema
