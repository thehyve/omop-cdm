"""OMOP CDM 5.4 derived elements tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from omop_cdm.constants import CDM_SCHEMA, FK_CONCEPT_ID, FK_PERSON_ID


class BaseConditionEraCdm54:
    __tablename__ = "condition_era"
    __table_args__ = {"schema": CDM_SCHEMA}

    condition_era_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    condition_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    condition_era_start_date: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=400)
    condition_era_end_date: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    condition_occurrence_count: Mapped[Optional[int]] = mapped_column(Integer, sort_order=600)

    @declared_attr
    def condition_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConditionEra.condition_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="ConditionEra.person_id")


class BaseDoseEraCdm54:
    __tablename__ = "dose_era"
    __table_args__ = {"schema": CDM_SCHEMA}

    dose_era_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    drug_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    unit_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=400)
    dose_value: Mapped[decimal.Decimal] = mapped_column(Numeric, sort_order=500)
    dose_era_start_date: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=600)
    dose_era_end_date: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=700)

    @declared_attr
    def drug_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DoseEra.drug_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="DoseEra.person_id")

    @declared_attr
    def unit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DoseEra.unit_concept_id")


class BaseDrugEraCdm54:
    __tablename__ = "drug_era"
    __table_args__ = {"schema": CDM_SCHEMA}

    drug_era_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    drug_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    drug_era_start_date: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=400)
    drug_era_end_date: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    drug_exposure_count: Mapped[Optional[int]] = mapped_column(Integer, sort_order=600)
    gap_days: Mapped[Optional[int]] = mapped_column(Integer, sort_order=700)

    @declared_attr
    def drug_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugEra.drug_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="DrugEra.person_id")


class BaseEpisodeCdm54:
    __tablename__ = "episode"
    __table_args__ = {"schema": CDM_SCHEMA}

    episode_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), sort_order=200)
    episode_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=300)
    episode_start_date: Mapped[datetime.date] = mapped_column(Date, sort_order=400)
    episode_start_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=500)
    episode_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=600)
    episode_end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, sort_order=700)
    episode_parent_id: Mapped[Optional[int]] = mapped_column(BigInteger, sort_order=800)
    episode_number: Mapped[Optional[int]] = mapped_column(Integer, sort_order=900)
    episode_object_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1000)
    episode_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1100)
    episode_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1200)
    episode_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1300)

    @declared_attr
    def episode_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Episode.episode_concept_id")

    @declared_attr
    def episode_object_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Episode.episode_object_concept_id")

    @declared_attr
    def episode_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Episode.episode_source_concept_id")

    @declared_attr
    def episode_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Episode.episode_type_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="Episode.person_id")


class BaseEpisodeEventCdm54:
    __tablename__ = "episode_event"
    __table_args__ = {"schema": CDM_SCHEMA}

    episode_id: Mapped[int] = mapped_column(
        ForeignKey(f"{CDM_SCHEMA}.episode.episode_id"), primary_key=True, sort_order=100
    )
    event_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=200)
    episode_event_field_concept_id: Mapped[int] = mapped_column(
        ForeignKey(FK_CONCEPT_ID), primary_key=True, sort_order=300
    )

    @declared_attr
    def episode_event_field_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="EpisodeEvent.episode_event_field_concept_id")

    @declared_attr
    def episode(cls) -> Mapped["Episode"]:
        return relationship("Episode", foreign_keys="EpisodeEvent.episode_id")
