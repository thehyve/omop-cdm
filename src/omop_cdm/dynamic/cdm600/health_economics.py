"""OMOP CDM 6.0.0 health economics tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import BigInteger, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

from omop_cdm.constants import CDM_SCHEMA, FK_CONCEPT_ID, FK_PERSON_ID


class BaseCostCdm600:
    __tablename__ = "cost"
    __table_args__ = {"schema": CDM_SCHEMA}

    cost_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    cost_event_id: Mapped[int] = mapped_column(BigInteger, sort_order=300)
    cost_event_field_concept_id: Mapped[int] = mapped_column(Integer, sort_order=400)
    cost_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=500)
    cost_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=600)
    currency_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=700)
    cost: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=800)
    incurred_date: Mapped[datetime.date] = mapped_column(Date, sort_order=900)
    billed_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=1000)
    paid_date: Mapped[Optional[datetime.date]] = mapped_column(Date, sort_order=1100)
    revenue_code_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1200)
    drg_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1300)
    cost_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1400)
    cost_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1500)
    revenue_code_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1600)
    drg_source_value: Mapped[Optional[str]] = mapped_column(String(3), sort_order=1700)
    payer_plan_period_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(f"{CDM_SCHEMA}.payer_plan_period.payer_plan_period_id"), sort_order=1800
    )

    @declared_attr
    def cost_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Cost.cost_concept_id")

    @declared_attr
    def cost_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Cost.cost_source_concept_id")

    @declared_attr
    def cost_type_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Cost.cost_type_concept_id")

    @declared_attr
    def currency_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Cost.currency_concept_id")

    @declared_attr
    def drg_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Cost.drg_concept_id")

    @declared_attr
    def payer_plan_period(cls) -> Mapped["PayerPlanPeriod"]:
        return relationship("PayerPlanPeriod", foreign_keys="Cost.payer_plan_period_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="Cost.person_id")

    @declared_attr
    def revenue_code_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Cost.revenue_code_concept_id")


class BasePayerPlanPeriodCdm600:
    __tablename__ = "payer_plan_period"
    __table_args__ = {"schema": CDM_SCHEMA}

    payer_plan_period_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    contract_person_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_PERSON_ID), sort_order=300)
    payer_plan_period_start_date: Mapped[datetime.date] = mapped_column(Date, sort_order=400)
    payer_plan_period_end_date: Mapped[datetime.date] = mapped_column(Date, sort_order=500)
    payer_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=600)
    plan_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=700)
    contract_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    sponsor_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=900)
    stop_reason_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1000)
    payer_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1100)
    payer_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1200)
    plan_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1300)
    plan_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1400)
    contract_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1500)
    contract_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1600)
    sponsor_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1700)
    sponsor_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1800)
    family_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1900)
    stop_reason_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=2000)
    stop_reason_source_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=2100)

    @declared_attr
    def contract_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.contract_concept_id")

    @declared_attr
    def contract_person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="PayerPlanPeriod.contract_person_id")

    @declared_attr
    def contract_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.contract_source_concept_id")

    @declared_attr
    def payer_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.payer_concept_id")

    @declared_attr
    def payer_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.payer_source_concept_id")

    @declared_attr
    def person(cls) -> Mapped["Person"]:
        return relationship("Person", foreign_keys="PayerPlanPeriod.person_id")

    @declared_attr
    def plan_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.plan_concept_id")

    @declared_attr
    def plan_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.plan_source_concept_id")

    @declared_attr
    def sponsor_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.sponsor_concept_id")

    @declared_attr
    def sponsor_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.sponsor_source_concept_id")

    @declared_attr
    def stop_reason_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.stop_reason_concept_id")

    @declared_attr
    def stop_reason_source_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="PayerPlanPeriod.stop_reason_source_concept_id")
