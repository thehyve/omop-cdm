from omop_cdm.constants import VOCAB_SCHEMA, CDM_SCHEMA
from pytest import fixture
from sqlalchemy import Engine, inspect

from tests.omop_cdm.dynamic.cdm_definitions import cdm600
from tests.omop_cdm.dynamic.conftest import create_all_tables, temp_schemas
from tests.omop_cdm.table_sets import VOCAB, CDM600_NON_VOCAB

SCHEMA_MAP = {
    VOCAB_SCHEMA: "vocab600",
    CDM_SCHEMA: "cdm600",
}


@fixture(scope="session")
def cdm600_engine(pg_db_engine: Engine) -> Engine:
    yield pg_db_engine.execution_options(schema_translate_map=SCHEMA_MAP)


def test_create_tables_cdm600(cdm600_engine: Engine):
    with temp_schemas(engine=cdm600_engine, schemas=set(SCHEMA_MAP.values())):
        create_all_tables(engine=cdm600_engine, metadata=cdm600.Base.metadata)
        vocab_tables = inspect(cdm600_engine).get_table_names(SCHEMA_MAP[VOCAB_SCHEMA])
        cdm_tables = inspect(cdm600_engine).get_table_names(SCHEMA_MAP[CDM_SCHEMA])
        assert set(vocab_tables) == VOCAB
        assert set(cdm_tables) == CDM600_NON_VOCAB
