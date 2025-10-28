import datetime

from sqlalchemy.orm import DeclarativeBase


def record_as_str(record: DeclarativeBase) -> str:
    col_name_values = {
        cname: str(getattr(record, cname))
        for cname in record.__class__.__table__.columns.keys()  # noqa: SIM118
    }
    return (
        f"{record.__class__.__name__}("
        f"""{
            ", ".join(
                f"{c_name}={c_value}" for c_name, c_value in col_name_values.items()
            )
        })"""
    )


def get_current_time_utc() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)
