"""OMOP CDM metadata tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from omop_cdm.constants import CDM_SCHEMA, FK_CONCEPT_ID


class BaseCdmSourceCdm54:
    __tablename__ = "cdm_source"
    __table_args__ = {"schema": CDM_SCHEMA}

    cdm_source_name: Mapped[str] = mapped_column(String(255), primary_key=True, sort_order=100)
    cdm_source_abbreviation: Mapped[str] = mapped_column(String(25), sort_order=200)
    cdm_holder: Mapped[str] = mapped_column(String(255), sort_order=300)
    source_description: Mapped[Optional[str]] = mapped_column(Text, sort_order=400)
    source_documentation_reference: Mapped[Optional[str]] = mapped_column(String(255), sort_order=500)
    cdm_etl_reference: Mapped[Optional[str]] = mapped_column(String(255), sort_order=600)
    source_release_date: Mapped[datetime.date] = mapped_column(Date, sort_order=700)
    cdm_release_date: Mapped[datetime.date] = mapped_column(Date, sort_order=800)
    cdm_version: Mapped[Optional[str]] = mapped_column(String(10), sort_order=900)
    cdm_version_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1000)
    vocabulary_version: Mapped[str] = mapped_column(String(20), sort_order=1100)

    @declared_attr
    def cdm_version_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="CdmSource.cdm_version_concept_id")


class BaseMetadataCdm54:
    __tablename__ = "metadata"
    __table_args__ = {"schema": CDM_SCHEMA}

    metadata_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=100)
    metadata_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=200)
    metadata_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=300)
    name: Mapped[str] = mapped_column(String(250), sort_order=400)
    value_as_string: Mapped[Optional[str]] = mapped_column(String(250), sort_order=500)
    value_as_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=600)
    value_as_number: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=700)
    metadata_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=800)
    metadata_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=900)

    @declared_attr
    def metadata_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Metadata.metadata_concept_id")

    @declared_attr
    def metadata_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Metadata.metadata_type_concept_id")

    @declared_attr
    def value_as_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Metadata.value_as_concept_id")
