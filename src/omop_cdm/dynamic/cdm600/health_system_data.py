"""OMOP CDM 6.0.0 health system tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import BigInteger, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from omop_cdm.constants import CDM_SCHEMA, FK_CARE_SITE_ID, FK_CONCEPT_ID, FK_LOCATION_ID


class BaseCareSiteCdm600:
    __tablename__ = "care_site"
    __table_args__ = {"schema": CDM_SCHEMA}

    care_site_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    care_site_name: Mapped[Optional[str]] = mapped_column(String(255), sort_order=200)
    place_of_service_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=300)
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_LOCATION_ID), sort_order=400)
    care_site_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=500)
    place_of_service_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=600)

    @declared_attr
    def location(cls) -> Mapped["Location"]:
        return relationship("Location", foreign_keys="CareSite.location_id")

    @declared_attr
    def place_of_service_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="CareSite.place_of_service_concept_id")


class BaseLocationCdm600:
    __tablename__ = "location"
    __table_args__ = {"schema": CDM_SCHEMA}

    location_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    address_1: Mapped[Optional[str]] = mapped_column(String(50), sort_order=200)
    address_2: Mapped[Optional[str]] = mapped_column(String(50), sort_order=300)
    city: Mapped[Optional[str]] = mapped_column(String(50), sort_order=400)
    state: Mapped[Optional[str]] = mapped_column(String(2), sort_order=500)
    zip: Mapped[Optional[str]] = mapped_column(String(9), sort_order=600)
    county: Mapped[Optional[str]] = mapped_column(String(20), sort_order=700)
    country: Mapped[Optional[str]] = mapped_column(String(100), sort_order=800)
    location_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=900)
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1000)
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1100)
    region_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1200)

    @declared_attr
    def region_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Location.region_concept_id")


class BaseLocationHistoryCdm600:
    __tablename__ = "location_history"
    __table_args__ = {"schema": CDM_SCHEMA}

    location_history_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    location_id: Mapped[int] = mapped_column(ForeignKey(FK_LOCATION_ID), sort_order=200)
    relationship_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=300)
    domain_id: Mapped[str] = mapped_column(String(50), sort_order=400)
    entity_id: Mapped[int] = mapped_column(BigInteger, sort_order=500)
    start_date: Mapped[datetime.date] = mapped_column(Date, sort_order=600)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=700)

    @declared_attr
    def location(cls) -> Mapped["Location"]:
        return relationship("Location", foreign_keys="LocationHistory.location_id")

    @declared_attr
    def relationship_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="LocationHistory.relationship_type_concept_id")


class BaseProviderCdm600:
    __tablename__ = "provider"
    __table_args__ = {"schema": CDM_SCHEMA}

    provider_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    provider_name: Mapped[Optional[str]] = mapped_column(String(255), sort_order=200)
    npi: Mapped[Optional[str]] = mapped_column(String(20), sort_order=300)
    dea: Mapped[Optional[str]] = mapped_column(String(20), sort_order=400)
    specialty_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=500)
    care_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CARE_SITE_ID), sort_order=600)
    year_of_birth: Mapped[Optional[int]] = mapped_column(Integer, sort_order=700)
    gender_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    provider_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=900)
    specialty_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1000)
    specialty_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1100)
    gender_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1200)
    gender_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1300)

    @declared_attr
    def care_site(cls) -> Mapped["CareSite"]:
        return relationship("CareSite", foreign_keys="Provider.care_site_id")

    @declared_attr
    def gender_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Provider.gender_concept_id")

    @declared_attr
    def gender_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Provider.gender_source_concept_id")

    @declared_attr
    def specialty_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Provider.specialty_concept_id")

    @declared_attr
    def specialty_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Provider.specialty_source_concept_id")
