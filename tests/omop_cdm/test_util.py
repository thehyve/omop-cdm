from datetime import date, datetime

from omop_cdm.regular.cdm54 import ObservationPeriod
from omop_cdm.util import get_current_time_utc, record_as_str


def test_record_is_converted_to_expected_string():
    op_record = ObservationPeriod(
        person_id=5, observation_period_start_date=date(2025, 11, 23)
    )
    expected_string = (
        "ObservationPeriod(observation_period_id=None, person_id=5, "
        "observation_period_start_date=2025-11-23, observation_period_end_date=None, "
        "period_type_concept_id=None)"
    )
    assert record_as_str(op_record) == expected_string
    # Converting a record to string should invoke the __repr__ method,
    # which in turn runs record_as_str. The result should therefore be
    # the same.
    assert str(op_record) == expected_string


def test_get_utc_time():
    utc_time = get_current_time_utc()
    assert isinstance(utc_time, datetime)
