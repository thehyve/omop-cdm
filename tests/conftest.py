from contextlib import contextmanager
from typing import Set

import pytest
from sqlalchemy import Connection, Engine, MetaData, create_engine
from sqlalchemy.sql.ddl import CreateSchema, DropSchema
from testcontainers.postgres import PostgresContainer

POSTGRES_IMAGE = "postgres:16-alpine"


@pytest.fixture(scope="session")
def pg_db_engine() -> Engine:
    with PostgresContainer(POSTGRES_IMAGE) as postgres:
        engine = create_engine(postgres.get_connection_url())
        yield engine


def create_schemas(schemas: Set[str], conn: Connection) -> None:
    for schema in schemas:
        conn.execute(CreateSchema(schema, if_not_exists=True))


def drop_schemas(schemas: Set[str], conn: Connection) -> None:
    for schema in schemas:
        conn.execute(DropSchema(schema, cascade=True, if_exists=True))


@contextmanager
def temp_schemas(engine: Engine, schemas: Set[str]):
    with engine.begin() as conn:
        create_schemas(schemas, conn)
    yield
    with engine.begin() as conn:
        drop_schemas(schemas, conn)


def create_all_tables(engine: Engine, metadata: MetaData) -> None:
    with engine.begin() as conn:
        metadata.create_all(bind=conn)
