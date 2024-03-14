"""OMOP CDM 6.0.0 derived elements tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from omop_cdm.constants import CDM_SCHEMA, FK_CONCEPT_ID, FK_PERSON_ID


class BaseConditionEraCdm600:
    __tablename__ = "condition_era"
    __table_args__ = {"schema": CDM_SCHEMA}

    condition_era_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    condition_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    condition_era_start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=400)
    condition_era_end_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    condition_occurrence_count: Mapped[Optional[int]] = mapped_column(Integer, sort_order=600)

    @declared_attr
    def condition_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="ConditionEra.condition_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="ConditionEra.person_id")


class BaseDoseEraCdm600:
    __tablename__ = "dose_era"
    __table_args__ = {"schema": CDM_SCHEMA}

    dose_era_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    drug_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    unit_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=400)
    dose_value: Mapped[decimal.Decimal] = mapped_column(Numeric, sort_order=500)
    dose_era_start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=600)
    dose_era_end_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=700)

    @declared_attr
    def drug_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DoseEra.drug_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="DoseEra.person_id")

    @declared_attr
    def unit_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DoseEra.unit_concept_id")


class BaseDrugEraCdm600:
    __tablename__ = "drug_era"
    __table_args__ = {"schema": CDM_SCHEMA}

    drug_era_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    drug_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), index=True, sort_order=300)
    drug_era_start_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=400)
    drug_era_end_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, sort_order=500)
    drug_exposure_count: Mapped[Optional[int]] = mapped_column(Integer, sort_order=600)
    gap_days: Mapped[Optional[int]] = mapped_column(Integer, sort_order=700)

    @declared_attr
    def drug_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="DrugEra.drug_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="DrugEra.person_id")
