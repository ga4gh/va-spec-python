"""Shared validator functions"""

from ga4gh.core.models import MappableConcept
from ga4gh.va_spec.base.enums import System


def validate_mappable_concept(
    mc: MappableConcept | None,
    valid_system: System,
    valid_codes: list[str],
    mc_is_required: bool = False,
) -> MappableConcept | None:
    """Validate GKS Core Mappable Concept object

    :param mc: Mappable Concept object
    :param valid_system: The system that should be used
    :param valid_codes: The codes that should be used
    :param mc_is_required: Whether or not `mc` is required
    :raises ValueError: If `mc` is invalid
    :return: Validated mappable concept
    """
    if not mc_is_required and not mc:
        return mc

    if not mc.primaryCoding:
        err_msg = "`primaryCoding` is required."
        raise ValueError(err_msg)

    if mc.primaryCoding.system != valid_system:
        err_msg = f"`primaryCoding.system` must be '{valid_system.value}'."
        raise ValueError(err_msg)

    if mc.primaryCoding.code.root not in valid_codes:
        err_msg = f"`primaryCoding.code` must be one of {valid_codes}."
        raise ValueError(err_msg)

    return mc
