from omop_cdm.constants import VOCAB_SCHEMA, CDM_SCHEMA
from pytest import fixture
from sqlalchemy import Engine, inspect

from tests.omop_cdm.dynamic.cdm_definitions import cdm54
from tests.omop_cdm.dynamic.conftest import create_all_tables, temp_schemas
from tests.omop_cdm.table_sets import VOCAB, CDM54_NON_VOCAB

SCHEMA_MAP = {
    VOCAB_SCHEMA: "vocab54",
    CDM_SCHEMA: "cdm54",
}


@fixture(scope="session")
def cdm54_engine(pg_db_engine: Engine) -> Engine:
    yield pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


def test_create_tables_cdm54(cdm54_engine: Engine):
    with temp_schemas(engine=cdm54_engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(engine=cdm54_engine, metadata=cdm54.Base.metadata)
        vocab_tables = inspect(cdm54_engine).get_table_names(SCHEMA_MAP[VOCAB_SCHEMA])
        cdm_tables = inspect(cdm54_engine).get_table_names(SCHEMA_MAP[CDM_SCHEMA])
        assert set(vocab_tables) == VOCAB
        assert set(cdm_tables) == CDM54_NON_VOCAB
