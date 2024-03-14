from copy import deepcopy

from sqlalchemy.orm import DeclarativeBase

from src.omop_cdm.dynamic.cdm54.clinical_data import BaseStemTableCdm54
from src.omop_cdm.dynamic.cdm54.vocabularies.vocabularies import (
    BaseSourceToConceptMapVersionCdm54,
)
from src.omop_cdm.regular.cdm54 import Base


# Workaround to avoid affecting the global scope via DeclarativeBase.
# Without it, the new tables added below would also affect the metadata
# property of BaseCdm54, meaning the extra tables would always be
# created when using BaseCdm54 instead of only for the relevant unit
# test.
class BaseCdm54Extended(DeclarativeBase):
    pass


metadata = deepcopy(Base.metadata)
BaseCdm54Extended.metadata = metadata


class SourceToConceptMapVersion(BaseSourceToConceptMapVersionCdm54, BaseCdm54Extended):
    pass


class StemTable(BaseStemTableCdm54, BaseCdm54Extended):
    pass
