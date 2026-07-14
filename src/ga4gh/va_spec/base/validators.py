"""Shared validator functions"""

import re
from enum import Enum
from types import MappingProxyType
from typing import ClassVar, Generic, TypeVar

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
    :raises ValueError: If `mc` is invalid or not provided when `mc_is_required`
        is set to True
    :return: Validated mappable concept
    """
    if not mc:
        if mc_is_required:
            msg = "MappableConcept is required"
            raise ValueError(msg)
        return None

    if not mc.primaryCoding:
        msg = "`primaryCoding` is required."
        raise ValueError(msg)

    coding = mc.primaryCoding
    code = coding.code.root

    if coding.system != valid_system:
        msg = f"`primaryCoding.system` must be '{valid_system.value}'."
        raise ValueError(msg)

    if valid_codes is not None and code not in valid_codes:
        msg = f"`primaryCoding.code` must be one of {valid_codes}."
        raise ValueError(msg)

    if code_pattern is not None and not re.match(code_pattern, code):
        msg = f"`primaryCoding.code` does not match regex pattern {code_pattern}."
        raise ValueError(msg)

    return mc


MethodTypeT = TypeVar("MethodTypeT", bound=Enum)
CriterionT = TypeVar("CriterionT", bound=Enum)


class MethodTypeCriterionValidationMixin(Generic[MethodTypeT, CriterionT]):
    """Mixin for validating method type and evidence outcome criterion.

    Should be used with classes that inherit from EvidenceLine
    """

    MethodType: ClassVar[type[MethodTypeT]]
    Criterion: ClassVar[type[CriterionT]]
    ALLOWED_CRITERIA_BY_METHOD_TYPE: ClassVar[
        MappingProxyType[MethodTypeT, frozenset[CriterionT]]
    ]
    METHOD_TYPE_BY_CRITERION: ClassVar[MappingProxyType[CriterionT, MethodTypeT]]

    def __init_subclass__(cls, **kwargs) -> None:
        """Initialize derived criterion mappings for a subclass.

        :param kwargs: Additional subclass initialization arguments.
        """
        super().__init_subclass__(**kwargs)

        allowed = cls.ALLOWED_CRITERIA_BY_METHOD_TYPE

        cls.METHOD_TYPE_BY_CRITERION = MappingProxyType(
            {
                criterion: method_type
                for method_type, criteria in allowed.items()
                for criterion in criteria
            }
        )

    @classmethod
    def _get_base_criterion_from_code(cls, evidence_outcome_code: str) -> CriterionT:
        """Return the base criterion from an evidence outcome code.

        The evidence outcome code may include a suffix with a leading
        underscore for adjusted strength. For example, 'PS3_moderate'.

        :param evidence_outcome_code: Evidence outcome code.
        :return: Base criterion.
        :raises ValueError: If ``evidence_outcome_code`` does not start with a
            valid criterion.
        """
        base_code = evidence_outcome_code.split("_", maxsplit=1)[0]

        try:
            return cls.Criterion(base_code)
        except ValueError as e:
            msg = f"Invalid Criterion: {base_code}"
            raise ValueError(msg) from e

    @classmethod
    def _validate_method_type_evidence_outcome(
        cls,
        method_type: str,
        evidence_outcome_code: str,
    ) -> None:
        """Validate that ``evidenceOutcome`` is compatible with a method type.

        :param method_type: Method type value from ``specifiedBy.methodType``.
        :param evidence_outcome_code: Evidence outcome to validate.
        :raises ValueError: If the evidence outcome criterion is invalid or is
            not valid for the specified method type.
        :return: None.
        """
        parsed_method_type = cls.MethodType(method_type)
        allowed_criteria = cls.ALLOWED_CRITERIA_BY_METHOD_TYPE[parsed_method_type]

        criterion = cls._get_base_criterion_from_code(evidence_outcome_code)

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
