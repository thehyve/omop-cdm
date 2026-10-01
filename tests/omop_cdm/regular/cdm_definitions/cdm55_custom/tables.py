from copy import deepcopy

from sqlalchemy.orm import DeclarativeBase

from src.omop_cdm.dynamic.cdm55.clinical_data import BaseStemTableCdm55
from src.omop_cdm.dynamic.cdm55.vocabularies.vocabularies import (
    BaseSourceToConceptMapVersionCdm55,
)
from src.omop_cdm.regular.cdm54 import Base


# Workaround to avoid affecting the global scope via DeclarativeBase.
# Without it, the new tables added below would also affect the metadata
# property of BaseCdm54, meaning the extra tables would always be
# created when using BaseCdm54 instead of only for the relevant unit
# test.
class BaseCdm55Extended(DeclarativeBase):
    pass


metadata = deepcopy(Base.metadata)
BaseCdm55Extended.metadata = metadata


class SourceToConceptMapVersion(BaseSourceToConceptMapVersionCdm55, BaseCdm55Extended):
    pass


class StemTable(BaseStemTableCdm55, BaseCdm55Extended):
    pass
