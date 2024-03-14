from omop_cdm.constants import VOCAB_SCHEMA, CDM_SCHEMA
from pytest import fixture
from sqlalchemy import Engine, inspect

from tests.omop_cdm.dynamic.cdm_definitions import cdm531
from tests.omop_cdm.dynamic.conftest import temp_schemas, create_all_tables
from tests.omop_cdm.table_sets import VOCAB, CDM531_NON_VOCAB

SCHEMA_MAP = {
    VOCAB_SCHEMA: "vocab531",
    CDM_SCHEMA: "cdm531",
}


@fixture(scope="session")
def cdm531_engine(pg_db_engine: Engine) -> Engine:
    yield pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


def test_create_tables_cdm531(cdm531_engine: Engine):
    with temp_schemas(engine=cdm531_engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(engine=cdm531_engine, metadata=cdm531.Base.metadata)
        vocab_tables = inspect(cdm531_engine).get_table_names(SCHEMA_MAP[VOCAB_SCHEMA])
        cdm_tables = inspect(cdm531_engine).get_table_names(SCHEMA_MAP[CDM_SCHEMA])
        assert set(vocab_tables) == VOCAB
        assert set(cdm_tables) == CDM531_NON_VOCAB
