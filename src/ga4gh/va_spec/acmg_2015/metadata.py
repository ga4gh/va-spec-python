"""Provide metadata for ACMG 2015 VA-Spec models."""

from ga4gh.va_spec.metadata import VASpecMetadataMixin


class ACMG2015MetadataMixin(VASpecMetadataMixin):
    """Provide metadata shared by models in the ACMG 2015 namespace."""

    _schema_namespace = "acmg-2015"
