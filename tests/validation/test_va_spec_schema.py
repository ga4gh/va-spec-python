"""Test that VA-Spec Python model structures match VA-Spec Schema"""

import json
from pathlib import Path
from typing import Literal, get_args, get_origin

import ga4gh.va_spec.profiles as va_spec_profiles

ROOT_DIR = Path(__file__).parents[2]
VA_SPEC_SCHEMA_DIR = (
    ROOT_DIR / "submodules" / "va_spec" / "schema" / "profiles" / "json"
)
VA_SPEC_SCHEMA = {}

VA_SPEC_BASE_CLASSES = set()
VA_SPEC_CONCRETE_CLASSES = set()
VA_SPEC_PRIMITIVES = set()


# Get profile classes
for f in VA_SPEC_SCHEMA_DIR.glob("*"):
    with f.open() as rf:
        cls_def = json.load(rf)

    va_spec_class = cls_def["title"]
    VA_SPEC_SCHEMA[va_spec_class] = cls_def

    if "properties" in cls_def:
        VA_SPEC_CONCRETE_CLASSES.add(va_spec_class)
    elif cls_def.get("type") in {"array", "integer", "string"}:
        VA_SPEC_PRIMITIVES.add(va_spec_class)
    else:
        VA_SPEC_BASE_CLASSES.add(va_spec_class)


def test_schema_models_in_pydantic():
    """Ensure that each schema model has corresponding Pydantic model"""
    for va_spec_class in (
        VA_SPEC_BASE_CLASSES | VA_SPEC_CONCRETE_CLASSES | VA_SPEC_PRIMITIVES
    ):
        assert getattr(va_spec_profiles, va_spec_class, False), va_spec_class


def test_schema_class_fields():
    """Check that each schema model properties exist and are required in corresponding
    Pydantic model, and validate required properties
    """
    for va_spec_class in VA_SPEC_CONCRETE_CLASSES:
        schema_properties = VA_SPEC_SCHEMA[va_spec_class]["properties"]
        pydantic_model = getattr(va_spec_profiles, va_spec_class)
        assert set(pydantic_model.model_fields) == set(schema_properties), va_spec_class

        required_schema_fields = set(VA_SPEC_SCHEMA[va_spec_class]["required"])

        for prop, property_def in schema_properties.items():
            pydantic_model_field_info = pydantic_model.model_fields[prop]
            pydantic_field_required = pydantic_model_field_info.is_required()

            if prop in required_schema_fields:
                if prop != "type":
                    if get_origin(pydantic_model_field_info.annotation) is Literal:
                        assert (
                            get_args(pydantic_model_field_info.annotation)[0]
                            == pydantic_model_field_info.default
                        )
                    else:
                        assert pydantic_field_required, f"{pydantic_model}.{prop}"
            else:
                assert not pydantic_field_required, f"{pydantic_model}.{prop}"

            if property_def.get("description") is not None:
                field_descr = pydantic_model_field_info.description or ""
                assert property_def["description"].replace(
                    "'", '"'
                ) == field_descr.replace("'", '"'), f"{pydantic_model}.{prop}"
            else:
                assert (
                    pydantic_model_field_info.description is None
                ), f"{pydantic_model}.{prop}"
