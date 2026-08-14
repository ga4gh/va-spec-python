"""Provide metadata for base VA-Spec models."""

from ga4gh.va_spec.metadata import VASpecMetadataMixin


class BaseMetadataMixin(VASpecMetadataMixin):
    """Provide metadata shared by models in the base namespace."""

    _schema_namespace = "base"
