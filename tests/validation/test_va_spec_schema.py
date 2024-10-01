"""Test that VA-Spec Python model structures match VA-Spec Schema"""

import json
from pathlib import Path

import ga4gh.va_spec.profiles as va_spec_profiles

ROOT_DIR = Path(__file__).parents[2]
VA_SPEC_SCHEMA_DIR = ROOT_DIR / "submodules" / "va_spec" / "schema"
VA_SPEC_SCHEMA = {}

VA_SPEC_CONCRETE_CLASSES = set()
VA_SPEC_PRIMITIVES = set()


def _update_classes_and_primitives(f_path: Path):
    with f_path.open() as rf:
        cls_def = json.load(rf)

    va_spec_class = cls_def["title"]
    VA_SPEC_SCHEMA[va_spec_class] = cls_def

    if "properties" in cls_def:
        VA_SPEC_CONCRETE_CLASSES.add(va_spec_class)
    elif cls_def.get("type") in {"array", "int", "str"}:
        VA_SPEC_PRIMITIVES.add(va_spec_class)


# Get profile classes
for child in (VA_SPEC_SCHEMA_DIR / "profiles").iterdir():
    for f in (child / "json").glob("*"):
        _update_classes_and_primitives(f)


def test_schema_models_exist():
    """Test that VA-Spec Python covers the models defined by VA-Spec"""
    for va_spec_class in VA_SPEC_CONCRETE_CLASSES | VA_SPEC_PRIMITIVES:
        assert getattr(va_spec_profiles, va_spec_class, False)


def test_schema_class_fields_are_valid():
    """Test that VA-Spec Python model fields match the VA-Spec specification"""
    for va_spec_class in VA_SPEC_CONCRETE_CLASSES:
        schema_fields = set(VA_SPEC_SCHEMA[va_spec_class]["properties"])
        pydantic_model = getattr(va_spec_profiles, va_spec_class)
        assert set(pydantic_model.model_fields) == schema_fields, va_spec_class


def test_model_keys_are_valid():
    """Test that digest keys on objects are valid and sorted"""
    for va_spec_class in VA_SPEC_CONCRETE_CLASSES:
        if (
            VA_SPEC_SCHEMA[va_spec_class].get("ga4ghDigest", {}).get("keys", None)
            is None
        ):
            continue

        pydantic_model = getattr(va_spec_profiles, va_spec_class)

        try:
            pydantic_model_digest_keys = pydantic_model.ga4gh.keys
        except AttributeError as e:
            raise AttributeError(va_spec_class) from e

        assert set(pydantic_model_digest_keys) == set(
            VA_SPEC_SCHEMA[va_spec_class]["ga4ghDigest"]["keys"]
        ), va_spec_class
        assert pydantic_model_digest_keys == sorted(
            pydantic_model.ga4gh.keys
        ), va_spec_class
