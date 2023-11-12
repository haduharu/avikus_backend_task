# schema.py
from pydantic import BaseModel, BaseConfig
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    created: datetime
    name: str
    content: bytes

    class Config(BaseConfig):
        orm_mode = True
        arbitrary_types_allowed = True