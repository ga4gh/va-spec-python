"""Provide JSON Schema metadata for VA-Spec models."""

from typing import ClassVar

from ga4gh.core.metadata import GKSMetadataMixin
from ga4gh.va_spec.version import VASPEC_VERSION


class VASpecMetadataMixin(GKSMetadataMixin):
    """Expose metadata for a concrete VA-Spec model."""

    _schema_namespace: ClassVar[str]
    _product_name = "va-spec"
    _product_version = VASPEC_VERSION

    @classmethod
    def schema_id(cls) -> str:
        """Return the model's canonical VA-Spec JSON Schema identifier."""
        return (
            f"{cls._schema_base_uri}/{cls._product_name}/{cls._product_version}/"
            f"{cls._schema_namespace}/json/{cls.__name__}"
        )
