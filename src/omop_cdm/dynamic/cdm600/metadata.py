"""OMOP CDM metadata tables."""

import datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from omop_cdm.constants import CDM_SCHEMA


class BaseCdmSourceCdm600:
    __tablename__ = "cdm_source"
    __table_args__ = {"schema": CDM_SCHEMA}

    cdm_source_name: Mapped[str] = mapped_column(String(255), primary_key=True, sort_order=100)
    cdm_source_abbreviation: Mapped[Optional[str]] = mapped_column(String(25), sort_order=200)
    cdm_holder: Mapped[Optional[str]] = mapped_column(String(255), sort_order=300)
    source_description: Mapped[Optional[str]] = mapped_column(Text, sort_order=400)
    source_documentation_reference: Mapped[Optional[str]] = mapped_column(String(255), sort_order=500)
    cdm_etl_reference: Mapped[Optional[str]] = mapped_column(String(255), sort_order=600)
    source_release_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=700)
    cdm_release_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=800)
    cdm_version: Mapped[Optional[str]] = mapped_column(String(10), sort_order=900)
    vocabulary_version: Mapped[Optional[str]] = mapped_column(String(20), sort_order=1000)


class BaseMetadataCdm600:
    __tablename__ = "metadata"
    __table_args__ = {"schema": CDM_SCHEMA}

    metadata_concept_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, sort_order=100)
    metadata_type_concept_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=200)
    name: Mapped[str] = mapped_column(String(250), primary_key=True, sort_order=300)
    value_as_string: Mapped[Optional[str]] = mapped_column(Text, sort_order=400)
    value_as_concept_id: Mapped[Optional[int]] = mapped_column(Integer, sort_order=500)
    metadata_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=600)
    metadata_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=700)
