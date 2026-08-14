"""Provide metadata for AAC 2017 VA-Spec models."""

from ga4gh.va_spec.metadata import VASpecMetadataMixin


class AAC2017MetadataMixin(VASpecMetadataMixin):
    """Provide metadata shared by models in the AAC 2017 namespace."""

    _schema_namespace = "aac-2017"
