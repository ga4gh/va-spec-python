"""Ensure that VA-Spec test fixtures validate against Pydantic models"""

import yaml
from ga4gh.va_spec import aac_2017, acmg_2015, base, ccv_2022

from tests.conftest import SUBMODULES_DIR, VaSpecSchema, get_va_spec_schema

VA_SPEC_TESTS_DIR = SUBMODULES_DIR / "tests"


with (VA_SPEC_TESTS_DIR / "test_definitions.yaml").open() as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
    test_definitions = data["tests"]

SCHEMA_TO_PYDANTIC_MODULE = {
    VaSpecSchema.AAC_2017: aac_2017,
    VaSpecSchema.ACMG_2015: acmg_2015,
    VaSpecSchema.CCV_2022: ccv_2022,
    VaSpecSchema.BASE: base,
}
VA_SPEC_TEST_DEFINITIONS = {schema: [] for schema in VaSpecSchema}


for test_def in test_definitions:
    if test_def["namespace"].startswith("va-spec."):
        schema = get_va_spec_schema(test_def["namespace"].split("va-spec.")[-1])
        VA_SPEC_TEST_DEFINITIONS[schema].append(test_def)


def test_va_spec_fixtures():
    """Test that VA-Spec test fixtures validate against Pydantic models"""
    for va_spec_schema, schema_test_defs in VA_SPEC_TEST_DEFINITIONS.items():
        pydantic_module = SCHEMA_TO_PYDANTIC_MODULE[va_spec_schema]

        for schema_test_def in schema_test_defs:
            with (
                VA_SPEC_TESTS_DIR / "fixtures" / schema_test_def["test_file"]
            ).open() as f:
                test_fixture_dict = yaml.load(f, Loader=yaml.SafeLoader)
                va_spec_class = schema_test_def["definition"]
                pydantic_model = getattr(pydantic_module, va_spec_class)
                assert pydantic_model(**test_fixture_dict)
