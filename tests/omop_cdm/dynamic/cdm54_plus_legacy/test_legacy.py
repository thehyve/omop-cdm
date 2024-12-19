import pytest
from sqlalchemy import Engine, inspect

from src.omop_cdm.constants import CDM_SCHEMA, VOCAB_SCHEMA
from tests.conftest import create_all_tables, temp_schemas, validate_relationships
from tests.omop_cdm.dynamic.cdm_definitions import cdm54_plus_legacy
from tests.omop_cdm.table_sets import CDM54_NON_VOCAB, CUSTOM, LEGACY, VOCAB

SCHEMA_MAP = {VOCAB_SCHEMA: "cdm54_legacy", CDM_SCHEMA: "cdm54_legacy"}


@pytest.fixture(scope="session")
def cdm54_legacy_engine(pg_db_engine: Engine) -> Engine:
    return pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


def test_create_tables_cdm54_plus_legacy(cdm54_legacy_engine: Engine):
    with temp_schemas(engine=cdm54_legacy_engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(
            engine=cdm54_legacy_engine, metadata=cdm54_plus_legacy.Base.metadata
        )
        cdm_tables = inspect(cdm54_legacy_engine).get_table_names(
            SCHEMA_MAP[CDM_SCHEMA]
        )
        assert set(cdm_tables) == VOCAB | CDM54_NON_VOCAB | LEGACY | CUSTOM
        validate_relationships(cdm54_legacy_engine, cdm54_plus_legacy.Person)
