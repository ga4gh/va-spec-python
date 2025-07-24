"""Provide utilities for test cases."""

from enum import Enum
from pathlib import Path

SUBMODULES_DIR = Path(__file__).parents[1] / "submodules" / "va_spec"


class VaSpecSchema(str, Enum):
    """Enum for VA-Spec schema"""

    AAC_2017 = "aac-2017"
    ACMG_2015 = "acmg-2015"
    BASE = "base"
    CCV_2022 = "ccv-2022"


def get_va_spec_schema(label: str) -> str | None:
    """Get VA-Spec schema given label

    :param label: Label
    :return: VA-Spec label
    """
    if label.endswith(VaSpecSchema.AAC_2017):
        schema = VaSpecSchema.AAC_2017
    elif label.endswith(VaSpecSchema.ACMG_2015):
        schema = VaSpecSchema.ACMG_2015
    elif label.endswith(VaSpecSchema.BASE):
        schema = VaSpecSchema.BASE
    elif label.endswith(VaSpecSchema.CCV_2022):
        schema = VaSpecSchema.CCV_2022
    else:
        schema = None
    return schema
