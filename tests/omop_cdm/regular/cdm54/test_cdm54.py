import pytest
from sqlalchemy import Engine, inspect

import src.omop_cdm.regular.cdm54 as cdm54
from src.omop_cdm.constants import CDM_SCHEMA, VOCAB_SCHEMA
from tests.conftest import create_all_tables, temp_schemas, validate_relationships
from tests.omop_cdm.table_sets import CDM54_NON_VOCAB, VOCAB

SCHEMA_MAP = {VOCAB_SCHEMA: "vocab54", CDM_SCHEMA: "cdm54"}


@pytest.fixture(scope="session")
def cdm54_regular_engine(pg_db_engine: Engine) -> Engine:
    return pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


def test_create_tables_cdm54_regular(cdm54_regular_engine: Engine):
    engine = cdm54_regular_engine
    with temp_schemas(engine=engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(engine=engine, metadata=cdm54.Base.metadata)
        vocab_tables = inspect(engine).get_table_names(SCHEMA_MAP[VOCAB_SCHEMA])
        cdm_tables = inspect(engine).get_table_names(SCHEMA_MAP[CDM_SCHEMA])
        assert set(vocab_tables) == VOCAB
        assert set(cdm_tables) == CDM54_NON_VOCAB
        validate_relationships(cdm54_regular_engine, cdm54.Person)
