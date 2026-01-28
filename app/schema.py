import uuid
from fastapi_users import schemas

from pydantic import BaseModel
import datetime
import pandas as pd

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass


class GraphReturn(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    graph_type: str
    data: dict
    created_at: datetime.datetime

class GraphParams(BaseModel):
    title: str
    graph_type: str
    df: pd.DataFrame
    x_label: str
    y_label: str
    has_y_int: bool = False
    y_int: float = None
