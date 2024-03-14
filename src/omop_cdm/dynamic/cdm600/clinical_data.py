"""OMOP CDM 6.0.0 clinical tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from omop_cdm.constants import (
    CDM_SCHEMA,
    FK_CARE_SITE_ID,
    FK_CONCEPT_ID,
    FK_DOMAIN_ID,
    FK_LOCATION_ID,
    FK_PERSON_ID,
    FK_PROVIDER_ID,
    FK_VISIT_DETAIL_ID,
    FK_VISIT_OCCURRENCE_ID,
)


class BaseFactRelationshipCdm600:
    __tablename__ = "fact_relationship"
    __table_args__ = {"schema": CDM_SCHEMA}

    fact_relationship_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=100)
    domain_concept_id_1: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=200)
    fact_id_1: Mapped[int] = mapped_column(Integer, sort_order=300)
    domain_concept_id_2: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=400)
    fact_id_2: Mapped[int] = mapped_column(Integer, sort_order=500)
    relationship_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=600)

    @declared_attr
    def domain_concept_1(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="FactRelationship.domain_concept_id_1")

    @declared_attr
    def domain_concept_2(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="FactRelationship.domain_concept_id_2")

    @declared_attr
    def relationship_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="FactRelationship.relationship_concept_id")


class BasePersonCdm600:
    __tablename__ = "person"
    __table_args__ = {"schema": CDM_SCHEMA}

    person_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    gender_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=200)
    year_of_birth: Mapped[int] = mapped_column(Integer, sort_order=300)
    month_of_birth: Mapped[Optional[int]] = mapped_column(Integer, sort_order=400)
    day_of_birth: Mapped[Optional[int]] = mapped_column(Integer, sort_order=500)
    birth_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=600)
    death_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=700)
    race_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    ethnicity_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=900)
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_LOCATION_ID), sort_order=1000)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=1100)
    care_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CARE_SITE_ID), sort_order=1200)
    person_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1300)
    gender_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1400)
    gender_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1500)
    race_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1600)
    race_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1700)
    ethnicity_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1800)
    ethnicity_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1900)

    @declared_attr
    def care_site(cls) -> Mapped["CareSite"]:
        return relationship("CareSite", foreign_keys="Person.care_site_id")

    @declared_attr
    def ethnicity_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Person.ethnicity_concept_id")

    @declared_attr
    def ethnicity_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Person.ethnicity_source_concept_id")

    @declared_attr
    def gender_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Person.gender_concept_id")

    @declared_attr
    def gender_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Person.gender_source_concept_id")

    @declared_attr
    def location(cls) -> Mapped["Location"]:
        return relationship("Location", foreign_keys="Person.location_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="Person.provider_id")

    @declared_attr
    def race_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Person.race_concept_id")

    @declared_attr
    def race_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Person.race_source_concept_id")


class BaseObservationPeriodCdm600:
    __tablename__ = "observation_period"
    __table_args__ = {"schema": CDM_SCHEMA}

    observation_period_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    observation_period_start_date: Mapped[datetime.date] = mapped_column(Date, sort_order=300)
    observation_period_end_date: Mapped[datetime.date] = mapped_column(Date, sort_order=400)
    period_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=500)

    @declared_attr
    def period_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ObservationPeriod.period_type_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="ObservationPeriod.person_id")


class BaseSpecimenCdm600:
    __tablename__ = "specimen"
    __table_args__ = {"schema": CDM_SCHEMA}

    specimen_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    specimen_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    specimen_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=400)
    specimen_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=500)
    specimen_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=600)
    quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=700)
    unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    anatomic_site_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=900)
    disease_status_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1000)
    specimen_source_id: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1100)
    specimen_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1200)
    unit_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1300)
    anatomic_site_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1400)
    disease_status_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1500)

    @declared_attr
    def anatomic_site_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Specimen.anatomic_site_concept_id")

    @declared_attr
    def disease_status_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Specimen.disease_status_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="Specimen.person_id")

    @declared_attr
    def specimen_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Specimen.specimen_concept_id")

    @declared_attr
    def specimen_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Specimen.specimen_type_concept_id")

    @declared_attr
    def unit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Specimen.unit_concept_id")


class BaseVisitOccurrenceCdm600:
    __tablename__ = "visit_occurrence"
    __table_args__ = {"schema": CDM_SCHEMA}

    visit_occurrence_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    visit_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    visit_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=400)
    visit_start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    visit_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=600)
    visit_end_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=700)
    visit_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=900)
    care_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CARE_SITE_ID), sort_order=1000)
    visit_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1100)
    visit_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1200)
    admitted_from_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1300)
    admitted_from_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1400)
    discharge_to_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1500)
    discharge_to_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1600)
    preceding_visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), sort_order=1700
    )

    @declared_attr
    def admitted_from_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitOccurrence.admitted_from_concept_id")

    @declared_attr
    def care_site(cls) -> Mapped["CareSite"]:
        return relationship("CareSite", foreign_keys="VisitOccurrence.care_site_id")

    @declared_attr
    def discharge_to_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitOccurrence.discharge_to_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="VisitOccurrence.person_id")

    @declared_attr
    def preceding_visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="VisitOccurrence.preceding_visit_occurrence_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="VisitOccurrence.provider_id")

    @declared_attr
    def visit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitOccurrence.visit_concept_id")

    @declared_attr
    def visit_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitOccurrence.visit_source_concept_id")

    @declared_attr
    def visit_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitOccurrence.visit_type_concept_id")


class BaseVisitDetailCdm600:
    __tablename__ = "visit_detail"
    __table_args__ = {"schema": CDM_SCHEMA}

    visit_detail_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    visit_detail_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    visit_detail_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=400)
    visit_detail_start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    visit_detail_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=600)
    visit_detail_end_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=700)
    visit_detail_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=900)
    care_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CARE_SITE_ID), sort_order=1000)
    discharge_to_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1100)
    admitted_from_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1200)
    admitted_from_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1300)
    visit_detail_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1400)
    visit_detail_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1500)
    discharge_to_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1600)
    preceding_visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=1700)
    visit_detail_parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=1800)
    visit_occurrence_id: Mapped[int] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), sort_order=1900)

    @declared_attr
    def admitted_from_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitDetail.admitted_from_concept_id")

    @declared_attr
    def care_site(cls) -> Mapped["CareSite"]:
        return relationship("CareSite", foreign_keys="VisitDetail.care_site_id")

    @declared_attr
    def discharge_to_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitDetail.discharge_to_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="VisitDetail.person_id")

    @declared_attr
    def preceding_visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="VisitDetail.preceding_visit_detail_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="VisitDetail.provider_id")

    @declared_attr
    def visit_detail_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitDetail.visit_detail_concept_id")

    @declared_attr
    def visit_detail_parent(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="VisitDetail.visit_detail_parent_id")

    @declared_attr
    def visit_detail_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitDetail.visit_detail_source_concept_id")

    @declared_attr
    def visit_detail_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="VisitDetail.visit_detail_type_concept_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="VisitDetail.visit_occurrence_id")


class BaseConditionOccurrenceCdm600:
    __tablename__ = "condition_occurrence"
    __table_args__ = {"schema": CDM_SCHEMA}

    condition_occurrence_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    condition_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    condition_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=400)
    condition_start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    condition_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=600)
    condition_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=700)
    condition_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    stop_reason: Mapped[Optional[str]] = mapped_column(String(20), sort_order=900)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=1000)
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True, sort_order=1100
    )
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=1200)
    condition_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1300)
    condition_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1400)
    condition_status_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1500)
    condition_status_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1600)

    @declared_attr
    def condition_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConditionOccurrence.condition_concept_id")

    @declared_attr
    def condition_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConditionOccurrence.condition_source_concept_id")

    @declared_attr
    def condition_status_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConditionOccurrence.condition_status_concept_id")

    @declared_attr
    def condition_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConditionOccurrence.condition_type_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="ConditionOccurrence.person_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="ConditionOccurrence.provider_id")

    @declared_attr
    def visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="ConditionOccurrence.visit_detail_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="ConditionOccurrence.visit_occurrence_id")


class BaseDeviceExposureCdm600:
    __tablename__ = "device_exposure"
    __table_args__ = {"schema": CDM_SCHEMA}

    device_exposure_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    device_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    device_exposure_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=400)
    device_exposure_start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    device_exposure_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=600)
    device_exposure_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=700)
    device_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    unique_device_id: Mapped[Optional[str]] = mapped_column(String(50), sort_order=900)
    quantity: Mapped[Optional[int]] = mapped_column(Integer, sort_order=1000)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=1100)
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True, sort_order=1200
    )
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=1300)
    device_source_value: Mapped[Optional[str]] = mapped_column(String(100), sort_order=1400)
    device_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1500)

    @declared_attr
    def device_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DeviceExposure.device_concept_id")

    @declared_attr
    def device_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DeviceExposure.device_source_concept_id")

    @declared_attr
    def device_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DeviceExposure.device_type_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="DeviceExposure.person_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="DeviceExposure.provider_id")

    @declared_attr
    def visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="DeviceExposure.visit_detail_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="DeviceExposure.visit_occurrence_id")


class BaseDrugExposureCdm600:
    __tablename__ = "drug_exposure"
    __table_args__ = {"schema": CDM_SCHEMA}

    drug_exposure_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    drug_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    drug_exposure_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=400)
    drug_exposure_start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    drug_exposure_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=600)
    drug_exposure_end_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=700)
    verbatim_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=800)
    drug_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=900)
    stop_reason: Mapped[Optional[str]] = mapped_column(String(20), sort_order=1000)
    refills: Mapped[Optional[int]] = mapped_column(Integer, sort_order=1100)
    quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1200)
    days_supply: Mapped[Optional[int]] = mapped_column(Integer, sort_order=1300)
    sig: Mapped[Optional[str]] = mapped_column(Text, sort_order=1400)
    route_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1500)
    lot_number: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1600)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=1700)
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True, sort_order=1800
    )
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=1900)
    drug_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=2000)
    drug_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=2100)
    route_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=2200)
    dose_unit_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=2300)

    @declared_attr
    def drug_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugExposure.drug_concept_id")

    @declared_attr
    def drug_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugExposure.drug_source_concept_id")

    @declared_attr
    def drug_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugExposure.drug_type_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="DrugExposure.person_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="DrugExposure.provider_id")

    @declared_attr
    def route_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugExposure.route_concept_id")

    @declared_attr
    def visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="DrugExposure.visit_detail_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="DrugExposure.visit_occurrence_id")


class BaseMeasurementCdm600:
    __tablename__ = "measurement"
    __table_args__ = {"schema": CDM_SCHEMA}

    measurement_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    measurement_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    measurement_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=400)
    measurement_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    measurement_time: Mapped[Optional[str]] = mapped_column(String(10), sort_order=600)
    measurement_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=700)
    operator_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    value_as_number: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=900)
    value_as_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1000)
    unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1100)
    range_low: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1200)
    range_high: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1300)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=1400)
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True, sort_order=1500
    )
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=1600)
    measurement_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1700)
    measurement_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1800)
    unit_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1900)
    value_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=2000)

    @declared_attr
    def measurement_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Measurement.measurement_concept_id")

    @declared_attr
    def measurement_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Measurement.measurement_source_concept_id")

    @declared_attr
    def measurement_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Measurement.measurement_type_concept_id")

    @declared_attr
    def operator_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Measurement.operator_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="Measurement.person_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="Measurement.provider_id")

    @declared_attr
    def unit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Measurement.unit_concept_id")

    @declared_attr
    def value_as_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Measurement.value_as_concept_id")

    @declared_attr
    def visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="Measurement.visit_detail_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="Measurement.visit_occurrence_id")


class BaseNoteCdm600:
    __tablename__ = "note"
    __table_args__ = {"schema": CDM_SCHEMA}

    note_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    note_event_id: Mapped[Optional[int]] = mapped_column(BigInteger, sort_order=300)
    note_event_field_concept_id: Mapped[int] = mapped_column(Integer, sort_order=400)
    note_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=500)
    note_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=600)
    note_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=700)
    note_class_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    note_title: Mapped[Optional[str]] = mapped_column(String(250), sort_order=900)
    note_text: Mapped[str] = mapped_column(Text, sort_order=1000)
    encoding_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1100)
    language_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1200)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=1300)
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True, sort_order=1400
    )
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=1500)
    note_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1600)

    @declared_attr
    def encoding_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Note.encoding_concept_id")

    @declared_attr
    def language_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Note.language_concept_id")

    @declared_attr
    def note_class_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Note.note_class_concept_id")

    @declared_attr
    def note_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Note.note_type_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="Note.person_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="Note.provider_id")

    @declared_attr
    def visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="Note.visit_detail_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="Note.visit_occurrence_id")


class BaseObservationCdm600:
    __tablename__ = "observation"
    __table_args__ = {"schema": CDM_SCHEMA}

    observation_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    observation_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    observation_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=400)
    observation_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    observation_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=600)
    value_as_number: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=700)
    value_as_string: Mapped[Optional[str]] = mapped_column(String(60), sort_order=800)
    value_as_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=900)
    value_as_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=1000)
    qualifier_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1100)
    unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1200)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=1300)
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True, sort_order=1400
    )
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=1500)
    observation_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1600)
    observation_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1700)
    unit_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1800)
    qualifier_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1900)
    observation_event_id: Mapped[Optional[int]] = mapped_column(BigInteger, sort_order=2000)
    obs_event_field_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=2100)

    @declared_attr
    def obs_event_field_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Observation.obs_event_field_concept_id")

    @declared_attr
    def observation_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Observation.observation_concept_id")

    @declared_attr
    def observation_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Observation.observation_source_concept_id")

    @declared_attr
    def observation_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Observation.observation_type_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="Observation.person_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="Observation.provider_id")

    @declared_attr
    def qualifier_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Observation.qualifier_concept_id")

    @declared_attr
    def unit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Observation.unit_concept_id")

    @declared_attr
    def value_as_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Observation.value_as_concept_id")

    @declared_attr
    def visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="Observation.visit_detail_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="Observation.visit_occurrence_id")


class BaseProcedureOccurrenceCdm600:
    __tablename__ = "procedure_occurrence"
    __table_args__ = {"schema": CDM_SCHEMA}

    procedure_occurrence_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    procedure_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    procedure_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=400)
    procedure_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    procedure_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=600)
    modifier_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=700)
    quantity: Mapped[Optional[int]] = mapped_column(Integer, sort_order=800)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=900)
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True, sort_order=1000
    )
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=1100)
    procedure_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1200)
    procedure_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1300)
    modifier_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1400)

    @declared_attr
    def modifier_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ProcedureOccurrence.modifier_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="ProcedureOccurrence.person_id")

    @declared_attr
    def procedure_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ProcedureOccurrence.procedure_concept_id")

    @declared_attr
    def procedure_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ProcedureOccurrence.procedure_source_concept_id")

    @declared_attr
    def procedure_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ProcedureOccurrence.procedure_type_concept_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="ProcedureOccurrence.provider_id")

    @declared_attr
    def visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="ProcedureOccurrence.visit_detail_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="ProcedureOccurrence.visit_occurrence_id")


class BaseSurveyConductCdm600:
    __tablename__ = "survey_conduct"
    __table_args__ = {"schema": CDM_SCHEMA}

    survey_conduct_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    survey_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=300)
    survey_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=400)
    survey_start_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=500)
    survey_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=600)
    survey_end_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=700)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=800)
    assisted_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=900)
    respondent_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1000)
    timing_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1100)
    collection_method_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1200)
    assisted_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1300)
    respondent_type_source_value: Mapped[Optional[str]] = mapped_column(String(100), sort_order=1400)
    timing_source_value: Mapped[Optional[str]] = mapped_column(String(100), sort_order=1500)
    collection_method_source_value: Mapped[Optional[str]] = mapped_column(String(100), sort_order=1600)
    survey_source_value: Mapped[Optional[str]] = mapped_column(String(100), sort_order=1700)
    survey_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1800)
    survey_source_identifier: Mapped[Optional[str]] = mapped_column(String(100), sort_order=1900)
    validated_survey_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=2000)
    validated_survey_source_value: Mapped[Optional[str]] = mapped_column(String(100), sort_order=2100)
    survey_version_number: Mapped[Optional[str]] = mapped_column(String(20), sort_order=2200)
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_OCCURRENCE_ID), sort_order=2300)
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=2400)
    response_visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), sort_order=2500
    )

    @declared_attr
    def assisted_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="SurveyConduct.assisted_concept_id")

    @declared_attr
    def collection_method_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="SurveyConduct.collection_method_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="SurveyConduct.person_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="SurveyConduct.provider_id")

    @declared_attr
    def respondent_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="SurveyConduct.respondent_type_concept_id")

    @declared_attr
    def response_visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="SurveyConduct.response_visit_occurrence_id")

    @declared_attr
    def survey_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="SurveyConduct.survey_concept_id")

    @declared_attr
    def survey_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="SurveyConduct.survey_source_concept_id")

    @declared_attr
    def timing_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="SurveyConduct.timing_concept_id")

    @declared_attr
    def validated_survey_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="SurveyConduct.validated_survey_concept_id")

    @declared_attr
    def visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="SurveyConduct.visit_detail_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="SurveyConduct.visit_occurrence_id")


class BaseNoteNlpCdm600:
    __tablename__ = "note_nlp"
    __table_args__ = {"schema": CDM_SCHEMA}

    note_nlp_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    note_id: Mapped[int] = mapped_column(ForeignKey(f"{CDM_SCHEMA}.note.note_id"), index=True, sort_order=200)
    section_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=300)
    snippet: Mapped[Optional[str]] = mapped_column(String(250), sort_order=400)
    offset: Mapped[Optional[str]] = mapped_column(String(250), sort_order=500)
    lexical_variant: Mapped[str] = mapped_column(String(250), sort_order=600)
    note_nlp_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=700)
    nlp_system: Mapped[Optional[str]] = mapped_column(String(250), sort_order=800)
    nlp_date: Mapped[datetime.date] = mapped_column(Date, sort_order=900)
    nlp_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=1000)
    term_exists: Mapped[Optional[str]] = mapped_column(String(1), sort_order=1100)
    term_temporal: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1200)
    term_modifiers: Mapped[Optional[str]] = mapped_column(String(2000), sort_order=1300)
    note_nlp_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1400)

    @declared_attr
    def note(cls) -> Mapped["Note"]:
        return relationship("Note", foreign_keys="NoteNlp.note_id")

    @declared_attr
    def note_nlp_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="NoteNlp.note_nlp_concept_id")

    @declared_attr
    def note_nlp_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="NoteNlp.note_nlp_source_concept_id")

    @declared_attr
    def section_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="NoteNlp.section_concept_id")


class BaseStemTableCdm600:
    __tablename__ = "stem_table"
    __table_args__ = {"schema": CDM_SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=100)
    domain_id: Mapped[Optional[str]] = mapped_column(ForeignKey(FK_DOMAIN_ID), sort_order=200)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=300)
    concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=400)
    start_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=500)
    start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=600)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=700)
    end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=800)
    verbatim_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=900)
    type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1000)
    operator_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1100)
    value_as_number: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1200)
    value_as_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1300)
    value_as_string: Mapped[Optional[str]] = mapped_column(String(60), sort_order=1400)
    value_as_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=1500)
    unit_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1600)
    range_low: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1700)
    range_high: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1800)
    provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PROVIDER_ID), sort_order=1900)
    visit_occurrence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(FK_VISIT_OCCURRENCE_ID), index=True, sort_order=2000
    )
    visit_detail_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_VISIT_DETAIL_ID), sort_order=2100)
    source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=2200)
    source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=2300)
    unit_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=2400)
    value_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=2500)
    stop_reason: Mapped[Optional[str]] = mapped_column(String(20), sort_order=2600)
    refills: Mapped[Optional[int]] = mapped_column(Integer, sort_order=2700)
    quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=2800)
    days_supply: Mapped[Optional[int]] = mapped_column(Integer, sort_order=2900)
    sig: Mapped[Optional[str]] = mapped_column(Text, sort_order=3000)
    route_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=3100)
    lot_number: Mapped[Optional[str]] = mapped_column(String(50), sort_order=3200)
    route_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=3300)
    dose_unit_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=3400)
    condition_status_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=3500)
    condition_status_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=3600)
    qualifier_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=3700)
    qualifier_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=3800)
    modifier_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=3900)
    unique_device_id: Mapped[Optional[str]] = mapped_column(String(50), sort_order=4000)
    anatomic_site_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=4100)
    disease_status_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=4200)
    specimen_source_id: Mapped[Optional[str]] = mapped_column(String(50), sort_order=4300)
    anatomic_site_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=4400)
    disease_status_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=4500)
    event_id: Mapped[Optional[int]] = mapped_column(BigInteger, sort_order=4600)
    event_field_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=4700)
    modifier_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=4800)

    @declared_attr
    def anatomic_site_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.anatomic_site_concept_id")

    @declared_attr
    def concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.concept_id")

    @declared_attr
    def condition_status_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.condition_status_concept_id")

    @declared_attr
    def disease_status_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.disease_status_concept_id")

    @declared_attr
    def domain(cls) -> Mapped["Domain"]:
        return relationship("Domain", foreign_keys="StemTable.domain_id")

    @declared_attr
    def event_field_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.event_field_concept_id")

    @declared_attr
    def modifier_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.modifier_concept_id")

    @declared_attr
    def operator_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.operator_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="StemTable.person_id")

    @declared_attr
    def provider(cls) -> Mapped["Provider"]:
        return relationship("Provider", foreign_keys="StemTable.provider_id")

    @declared_attr
    def qualifier_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.qualifier_concept_id")

    @declared_attr
    def route_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.route_concept_id")

    @declared_attr
    def source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.source_concept_id")

    @declared_attr
    def type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.type_concept_id")

    @declared_attr
    def unit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.unit_concept_id")

    @declared_attr
    def value_as_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="StemTable.value_as_concept_id")

    @declared_attr
    def visit_detail(cls) -> Mapped["VisitDetail"]:
        return relationship("VisitDetail", foreign_keys="StemTable.visit_detail_id")

    @declared_attr
    def visit_occurrence(cls) -> Mapped["VisitOccurrence"]:
        return relationship("VisitOccurrence", foreign_keys="StemTable.visit_occurrence_id")
