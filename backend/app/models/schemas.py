from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from enum import Enum

class RepositoryStatus(str, Enum):
    pending = "pending"
    success = "success"
    error = "error"

class RepositoryRequest(BaseModel):
    url: HttpUrl
    branch: str = Field(default="main", min_length=1, strip_whitespace=True)

class RepositoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    url: HttpUrl
    branch: str
    status: RepositoryStatus
