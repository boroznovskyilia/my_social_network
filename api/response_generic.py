from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel

DataType = TypeVar("DataType")

class IResponseBase(BaseModel, Generic[DataType]):
    status: Optional[str] = None
    data: Optional[DataType] = None
