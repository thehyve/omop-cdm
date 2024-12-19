import pytest
from sqlalchemy import BIGINT, Engine, inspect

from src.omop_cdm.constants import CDM_SCHEMA, VOCAB_SCHEMA
from tests.conftest import create_all_tables, temp_schemas, validate_relationships
from tests.omop_cdm.dynamic.cdm_definitions import cdm54_custom
from tests.omop_cdm.table_sets import CDM54_NON_VOCAB, CUSTOM

SCHEMA_MAP = {VOCAB_SCHEMA: "vocab54_custom", CDM_SCHEMA: "cdm54_custom"}


@pytest.fixture(scope="session")
def cdm54_custom_engine(pg_db_engine: Engine) -> Engine:
    return pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


@pytest.fixture(scope="module")
def _create_custom_cdm_tables(cdm54_custom_engine: Engine):
    with temp_schemas(engine=cdm54_custom_engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(
            engine=cdm54_custom_engine, metadata=cdm54_custom.Base.metadata
        )
        yield


@pytest.mark.usefixtures("_create_custom_cdm_tables")
def test_custom_table_is_created(cdm54_custom_engine: Engine):
    cdm_tables = inspect(cdm54_custom_engine).get_table_names(SCHEMA_MAP[CDM_SCHEMA])
    assert set(cdm_tables) == CDM54_NON_VOCAB | CUSTOM | {"cloudspine"}
    validate_relationships(cdm54_custom_engine, cdm54_custom.Person)


@pytest.mark.usefixtures("_create_custom_cdm_tables")
def test_column_can_be_redefined(cdm54_custom_engine: Engine):
    """person.person_id data type should be bigint."""
    person_columns = inspect(cdm54_custom_engine).get_columns(
        table_name="person", schema=SCHEMA_MAP[CDM_SCHEMA]
    )
    person_id = person_columns[0]
    assert person_id["name"] == "person_id"
    assert isinstance(person_id["type"], BIGINT)


@pytest.mark.usefixtures("_create_custom_cdm_tables")
def test_custom_columns_can_be_added(cdm54_custom_engine: Engine):
    """Custom columns are added in the expected position."""
    death_columns = inspect(cdm54_custom_engine).get_columns(
        table_name="death", schema=SCHEMA_MAP[CDM_SCHEMA]
    )
    death_columns = [c["name"] for c in death_columns]
    assert death_columns == [
        "person_id",
        "new_field_1",
        "death_date",
        "death_datetime",
        "death_type_concept_id",
        "cause_concept_id",
        "cause_source_value",
        "cause_source_concept_id",
        "new_field_2",
    ]
