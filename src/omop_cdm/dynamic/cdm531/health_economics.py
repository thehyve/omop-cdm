"""OMOP CDM 5.3.1 health economics tables."""

import datetime
import decimal
from typing import Optional

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from omop_cdm.constants import CDM_SCHEMA, FK_CONCEPT_ID, FK_DOMAIN_ID, FK_PERSON_ID


class BasePayerPlanPeriodCdm531:
    __tablename__ = "payer_plan_period"
    __table_args__ = {"schema": CDM_SCHEMA}

    payer_plan_period_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=100)
    person_id: Mapped[int] = mapped_column(ForeignKey(FK_PERSON_ID), index=True, sort_order=200)
    payer_plan_period_start_date: Mapped[datetime.date] = mapped_column(Date, sort_order=300)
    payer_plan_period_end_date: Mapped[datetime.date] = mapped_column(Date, sort_order=400)
    payer_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=500)
    payer_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=600)
    payer_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=700)
    plan_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=800)
    plan_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=900)
    plan_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1000)
    sponsor_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1100)
    sponsor_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1200)
    sponsor_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1300)
    family_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1400)
    stop_reason_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1500)
    stop_reason_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=1600)
    stop_reason_source_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1700)

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


class BaseCostCdm531:
    __tablename__ = "cost"
    __table_args__ = {"schema": CDM_SCHEMA}

    cost_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=100)
    cost_event_id: Mapped[int] = mapped_column(Integer, sort_order=200)
    cost_domain_id: Mapped[str] = mapped_column(ForeignKey(FK_DOMAIN_ID), sort_order=300)
    cost_type_concept_id: Mapped[int] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=400)
    currency_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=500)
    total_charge: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=600)
    total_cost: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=700)
    total_paid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=800)
    paid_by_payer: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=900)
    paid_by_patient: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1000)
    paid_patient_copay: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1100)
    paid_patient_coinsurance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1200)
    paid_patient_deductible: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1300)
    paid_by_primary: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1400)
    paid_ingredient_cost: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1500)
    paid_dispensing_fee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1600)
    payer_plan_period_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(f"{CDM_SCHEMA}.payer_plan_period.payer_plan_period_id"), sort_order=1700
    )
    amount_allowed: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, sort_order=1800)
    revenue_code_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=1900)
    revenue_code_source_value: Mapped[Optional[str]] = mapped_column(String(50), sort_order=2000)
    drg_concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey(FK_CONCEPT_ID), sort_order=2100)
    drg_source_value: Mapped[Optional[str]] = mapped_column(String(3), sort_order=2200)

    @declared_attr
    def cost_domain(cls) -> Mapped["Domain"]:
        return relationship("Domain", foreign_keys="Cost.cost_domain_id")

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
    def revenue_code_concept(cls) -> Mapped["Concept"]:
        return relationship("Concept", foreign_keys="Cost.revenue_code_concept_id")
