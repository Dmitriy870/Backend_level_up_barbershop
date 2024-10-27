from datetime import datetime,time
from typing import Any
from pydantic import BaseModel,ConfigDict


class BaseService(BaseModel):
    name: str
    description: str
    price: float
    execution_time: time


class CreateService(BaseService):
    image: bytes | None = None

class Service(CreateService):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ServiceRespon(BaseService):
    id: int
    avatar_base64: Any