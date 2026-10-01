import pytest
from sqlalchemy import Engine, inspect

from src.omop_cdm.constants import CDM_SCHEMA, VOCAB_SCHEMA
from tests.conftest import create_all_tables, temp_schemas, validate_relationships
from tests.omop_cdm.dynamic.cdm_definitions import cdm55_plus_legacy
from tests.omop_cdm.table_sets import CDM55_NON_VOCAB, CUSTOM, LEGACY, VOCAB_CDM55

SCHEMA_MAP = {VOCAB_SCHEMA: "cdm55_legacy", CDM_SCHEMA: "cdm55_legacy"}


@pytest.fixture(scope="session")
def cdm55_legacy_engine(pg_db_engine: Engine) -> Engine:
    return pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


def test_create_tables_cdm55_plus_legacy(cdm55_legacy_engine: Engine):
    with temp_schemas(engine=cdm55_legacy_engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(
            engine=cdm55_legacy_engine, metadata=cdm55_plus_legacy.Base.metadata
        )
        cdm_tables = inspect(cdm55_legacy_engine).get_table_names(
            SCHEMA_MAP[CDM_SCHEMA]
        )
        assert set(cdm_tables) == VOCAB_CDM55 | CDM55_NON_VOCAB | LEGACY | CUSTOM
        validate_relationships(cdm55_legacy_engine, cdm55_plus_legacy.Person)
