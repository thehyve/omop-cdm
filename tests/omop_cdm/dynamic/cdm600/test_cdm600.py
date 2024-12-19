import pytest
from sqlalchemy import Engine, inspect

from src.omop_cdm.constants import CDM_SCHEMA, VOCAB_SCHEMA
from tests.conftest import create_all_tables, temp_schemas, validate_relationships
from tests.omop_cdm.dynamic.cdm_definitions import cdm600
from tests.omop_cdm.table_sets import CDM600_NON_VOCAB, CUSTOM, VOCAB

SCHEMA_MAP = {VOCAB_SCHEMA: "vocab600", CDM_SCHEMA: "cdm600"}


@pytest.fixture(scope="session")
def cdm600_engine(pg_db_engine: Engine) -> Engine:
    return pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


def test_create_tables_cdm600(cdm600_engine: Engine):
    with temp_schemas(engine=cdm600_engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(engine=cdm600_engine, metadata=cdm600.Base.metadata)
        vocab_tables = inspect(cdm600_engine).get_table_names(SCHEMA_MAP[VOCAB_SCHEMA])
        cdm_tables = inspect(cdm600_engine).get_table_names(SCHEMA_MAP[CDM_SCHEMA])
        assert set(vocab_tables) == VOCAB
        assert set(cdm_tables) == CDM600_NON_VOCAB | CUSTOM
        validate_relationships(cdm600_engine, cdm600.Person)
