import pytest
from sqlalchemy import Engine, inspect

from src.omop_cdm.constants import CDM_SCHEMA, VOCAB_SCHEMA
from tests.conftest import create_all_tables, temp_schemas
from tests.omop_cdm.regular.cdm_definitions.cdm54_custom import BaseCdm54Extended
from tests.omop_cdm.table_sets import CDM54_NON_VOCAB, CUSTOM, VOCAB

SCHEMA_MAP = {VOCAB_SCHEMA: "vocab54_custom", CDM_SCHEMA: "cdm54_custom"}


@pytest.fixture(scope="session")
def cdm54_extra_tables_engine(pg_db_engine: Engine) -> Engine:
    return pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


def test_create_tables_cdm54_extra_tables(cdm54_extra_tables_engine: Engine):
    engine = cdm54_extra_tables_engine
    with temp_schemas(engine=engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(engine=engine, metadata=BaseCdm54Extended.metadata)
        vocab_tables = inspect(engine).get_table_names(SCHEMA_MAP[VOCAB_SCHEMA])
        cdm_tables = inspect(engine).get_table_names(SCHEMA_MAP[CDM_SCHEMA])
        assert set(vocab_tables) == VOCAB
        assert set(cdm_tables) == CDM54_NON_VOCAB | CUSTOM
