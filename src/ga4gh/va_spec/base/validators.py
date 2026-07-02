"""Shared validator functions"""

import re
from enum import Enum
from types import MappingProxyType
from typing import TypeVar

from ga4gh.core.models import MappableConcept
from ga4gh.va_spec.base.enums import System


def validate_mappable_concept(
    mc: MappableConcept | None,
    valid_system: System,
    valid_codes: list[str] | None = None,
    code_pattern: str | None = None,
    mc_is_required: bool = False,
) -> MappableConcept | None:
    """Validate GKS Core Mappable Concept object

    :param mc: Mappable Concept object
    :param valid_system: The system that should be used
    :param valid_codes: The codes that should be used for ``primaryCoding.code``
    :param code_pattern: The regex pattern that should be used for
        ``primaryCoding.code``
    :param mc_is_required: Whether or not `mc` is required
    :raises ValueError: If `mc` is invalid
    :return: Validated mappable concept
    """
    if not mc_is_required and not mc:
        return mc

    if mc and not mc.primaryCoding:
        err_msg = "`primaryCoding` is required."
        raise ValueError(err_msg)

    if mc and mc.primaryCoding.system != valid_system:
        err_msg = f"`primaryCoding.system` must be '{valid_system.value}'."
        raise ValueError(err_msg)

    if valid_codes is not None and mc.primaryCoding.code.root not in valid_codes:
        err_msg = f"`primaryCoding.code` must be one of {valid_codes}."
        raise ValueError(err_msg)

    if code_pattern is not None and not re.match(
        code_pattern, mc.primaryCoding.code.root
    ):
        err_msg = f"`primaryCoding.code` does not match regex pattern {code_pattern}."
        raise ValueError(err_msg)

    return mc


_MethodTypeT = TypeVar("MethodTypeT", bound=Enum)
_CriterionT = TypeVar("CriterionT", bound=Enum)


def _validate_method_type_evidence_outcome(
    method_type_enum: type[_MethodTypeT],
    method_type: str,
    criterion_enum: type[_CriterionT],
    allowed_criteria_by_method_type: MappingProxyType[
        _MethodTypeT, frozenset[type[_CriterionT]]
    ],
    evidence_outcome_code: str,
) -> None:
    """Validate that ``evidenceOutcome`` is compatible with a method type.

    :param method_type_enum: Enum class for valid method types.
    :param method_type: Method type value from ``specifiedBy.methodType``.
    :param criterion_enum: Enum class for valid evidence outcomes.
    :param allowed_criteria_by_method_type: Mapping of allowed criteria per
        mapping type.
    :param evidence_outcome_code: Evidence outcome code to validate.
    :raises ValueError: If the evidence outcome criterion is invalid or is
        not valid for the specified method type.
    """

    def _get_base_criterion_from_code(
        criterion: type[_CriterionT], evidence_outcome_code: str
    ) -> _CriterionT:
        """Return the base criterion from an evidence outcome code.

        The evidence outcome code may include a suffix with a leading
        underscore for adjusted strength. For example, 'PS3_moderate'.

        :param criterion: Enum class for valid evidence outcomes.
        :param evidence_outcome_code: Evidence outcome code to validate.
        :return: Base criterion.
        :raises ValueError: If ``evidence_outcome_code`` does not start with a
            valid criterion.
        """
        base_code = evidence_outcome_code.split("_", maxsplit=1)[0]

        try:
            return criterion(base_code)
        except ValueError as e:
            msg = f"Invalid Criterion: {base_code}"
            raise ValueError(msg) from e

    parsed_method_type = method_type_enum(method_type)
    allowed_criteria = allowed_criteria_by_method_type[parsed_method_type]

    criterion = _get_base_criterion_from_code(criterion_enum, evidence_outcome_code)

    if criterion not in allowed_criteria:
        allowed_values = ", ".join(
            sorted(allowed.value for allowed in allowed_criteria)
        )
        msg = (
            f"Invalid evidenceOutcome criterion '{criterion.value}' for "
            f"specifiedBy.methodType '{method_type}'. "
            f"Expected one of: {allowed_values}"
        )
        raise ValueError(msg)
