import pytest
from sqlalchemy import Engine, inspect

import src.omop_cdm.regular.cdm55 as cdm55
from src.omop_cdm.constants import CDM_SCHEMA, VOCAB_SCHEMA
from tests.conftest import create_all_tables, temp_schemas, validate_relationships
from tests.omop_cdm.table_sets import CDM55_NON_VOCAB, VOCAB_CDM55

SCHEMA_MAP = {VOCAB_SCHEMA: "vocab55", CDM_SCHEMA: "cdm55"}


@pytest.fixture(scope="session")
def cdm55_regular_engine(pg_db_engine: Engine) -> Engine:
    return pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


def test_create_tables_cdm55_regular(cdm55_regular_engine: Engine):
    engine = cdm55_regular_engine
    with temp_schemas(engine=engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(engine=engine, metadata=cdm55.Base.metadata)
        vocab_tables = inspect(engine).get_table_names(SCHEMA_MAP[VOCAB_SCHEMA])
        cdm_tables = inspect(engine).get_table_names(SCHEMA_MAP[CDM_SCHEMA])
        assert set(vocab_tables) == VOCAB_CDM55
        assert set(cdm_tables) == CDM55_NON_VOCAB
        validate_relationships(cdm55_regular_engine, cdm55.Person)
