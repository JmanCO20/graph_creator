import uuid
from fastapi_users import schemas

from pydantic import BaseModel, ConfigDict
from typing import Any

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class GraphParams(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    labels: dict[str, str]
    graph_type: str
    df: list[dict[str, Any]]
    checkboxes: dict[str, bool | float | None]
    trendlines: dict[str, bool]
    window_size: dict[str, None | float]
    previous_lines: dict[str, list | None]
