# Usage

omop-cdm provides SQLAlchemy declarative table definitions that can be used
to interact with an OMOP CDM via Python. This can be to more easily create all tables in
your database, but also to use them for data manipulation
(see [SQLAlchemy data manipulation](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html)).

## Preparation

Before creating the OMOP CDM tables, the following must be available:

- Target database
- Schema (or schemas) in which to create the tables

## Schemas

omop-cdm uses placeholders for the schema names, which are intended to be
replaced by the desired schema names. This can be done via the `schema_translate_map`
property of SQLAlchemy. By default, the vocabulary tables have a different schema
than the other tables, but both placeholders can be mapped to the same target
schema, to make sure all tables are in a single schema (recommended).

This example shows how to set a single schema "cdm54" via the SQLAlchemy engine:
```python
from omop_cdm.constants import CDM_SCHEMA, VOCAB_SCHEMA
from sqlalchemy import create_engine


OMOP_SCHEMA = "cdm54"

schema_map = {
    CDM_SCHEMA: OMOP_SCHEMA,
    VOCAB_SCHEMA: OMOP_SCHEMA,
}

engine = create_engine("postgresql://postgres@localhost/mydb")
engine = engine.execution_options(schema_translate_map=schema_map)
```

## Regular vs Dynamic CDM

The CDM table definitions of a particular CDM release can be imported in two different
ways.

### Regular
To use a standard set of CDM tables, you can import the module containing the
definitions as follows:
```python
from omop_cdm.regular import cdm54
```
In this regular fashion, all tables are already bound to a SQLAlchemy
`DeclarativeBase` class. This approach leaves fewer options for CDM modification,
but is slightly simpler to use.

E.g. once the engine is defined, creating all the tables in a database can be done
by simply running the following:

```python
with engine.begin() as conn:
    cdm54.Base.metadata.create_all(bind=conn)
```

### Dynamic

Alternatively, you can use the dynamic CDM definitions. Here tables have not been bound to
a SQLAlchemy `DeclarativeBase` class yet, but are defined as regular classes, which can
then be used as [mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html).

To use these, the classes must first be bound to a `Base`:
```python
from omop_cdm.dynamic import cdm54
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Person(cdm54.BasePersonCdm54, Base):
    pass

# Etc. for all other tables
```
This approach allows for the greatest customization possibilities.

Additionally, the dynamic version includes two additional tables which can optionally
be added to your CDM. These are the `StemTable` (intermediate table for mapping purposes)
and the `StcmVersion` table (to allow versioning of STCM source vocabulary mappings).

## Legacy tables

Apart from the standard CDM tables, the following legacy table classes can be
added to your CDM by binding them to your `DeclarativeBase`:

- AttributeDefinition
- Cohort
- CohortAttribute
- CohortDefinition

These tables have been part of the standard CDM in previous releases, but have since been moved
to the results schema or removed entirely.

They can be imported from `omop_cdm.dynamic.legacy`.

## Customizing the CDM

> **_NOTE:_** When adding or replacing columns, you can determine the position of the column in the table by setting
a ``sort_order`` value inside ``mapped_column()``. The default CDM table columns have a ``sort_order``
value pre-assigned with increments of 100 (column1 = 100, column2 = 200, etc.). This only works for tables
> imported from the dynamic module.

### New columns
If desired, you can add custom fields to existing CDM tables.
For dynamic tables, define the table class as normal, but add additional `mapped_column` fields with the
data types of choice. E.g. to add an integer column to the person table:

```python
class Person(BasePersonCdm54, Base):
    favorite_number: Mapped[Optional[int]] = mapped_column(Integer)
```

For tables from the regular modules, use the following syntax:
```python
Person.favorite_number = Column(Integer, nullable=True)
```


### Replace columns

> **_NOTE:_** Replacing columns is only possible with dynamic table definitions.

Although not recommended, you can replace existing CDM table columns with a different type of column.
E.g. removing the character limit of the `ethnicity_source_value` column in the person table, by replacing
it with a `Text` data type, can be done as follows:

```python
from typing import Optional

from omop_cdm.dynamic import cdm54 as cdm
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


class Person(cdm.BasePersonCdm54, Base):
    ethnicity_source_value: Mapped[Optional[str]] = mapped_column(Text)
```

It's important to note that replacing columns can only be done if the replacement
doesn't break relationships with other tables.
For example, replacing the `Integer` `person_id` column with `BigInteger` in the person table
is possible. Replacing it with a column of type ``Text`` is not, as it breaks FK relationships
that other CDM tables have with this field.

### Replace whole table

> **_NOTE:_** Replacing tables is only possible with dynamic table definitions.

Instead of adding or replacing individual columns, it's also possible to replace an entire table.
To do that, remove the inherited table base class from your table class and define all fields yourself.
E.g. for the person table:

```python
from omop_cdm.constants import CDM_SCHEMA

class Person(Base):
    __tablename__ = "person"
    __table_args__ = {"schema": CDM_SCHEMA}
    # Define all columns here
```

Just like with modifying individual columns, this will only work if no violations occur in relationships
with other CDM tables.

Add new tables
--------------
In addition to the default CDM tables, you can also add your own custom tables to the model.

By adding these tables to the same `DeclarativeBase` as the regular tables, they will become part
of the ORM. For example:

```python
from omop_cdm.constants import CDM_SCHEMA
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Narcissus(Base):
    __tablename__ = 'narcissus'
    __table_args__ = {'schema': CDM_SCHEMA}

    person_id: Mapped[int] = mapped_column(ForeignKey('cdm_schema.person.person_id'))
    loved_by_narcissus: Mapped[bool] = mapped_column(Boolean, default=False)

    person: Mapped["Person"] = relationship("Person")
```

### Schema name
When adding your own tables, it's a good practice to specify a schema name via ``__table_args__``
(see example above). If the schema will always be the same, there is no harm in hard coding the name.
Otherwise, it's better to provide the schema placeholder name, and let the runtime schema name be
determined by your `schema_translate_map`.


## Querying the CDM

Starting from CDM 5.4, all table relationships are accessible via ORM attributes.
In the example below, a populated CDM is queried by finding a person given a
person_source_value. Then all condition start dates and concept names are listed
for that person.

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from omop_cdm.constants import CDM_SCHEMA, VOCAB_SCHEMA
from omop_cdm.regular import cdm54

schema_map = {
    CDM_SCHEMA: "cdm54",
    VOCAB_SCHEMA: "vocab",
}

engine = create_engine("postgresql://postgres@localhost/ohdsi")
engine = engine.execution_options(schema_translate_map=schema_map)

with Session(engine) as session:
    statement = select(cdm54.Person).filter_by(person_source_value="0009456b")
    person: cdm54.Person = session.scalars(statement).one()
    conditions = person.condition_occurrences

    for c in conditions:
        print(c.condition_start_date, c.condition_concept.concept_name)
```
