import uuid
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TODOStatusEnum(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class TODOEntity(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    name: str
    status: TODOStatusEnum = TODOStatusEnum.PENDING
    description: str

    def change_transition(self, status: TODOStatusEnum):
        if self.status == TODOStatusEnum.COMPLETED:
            raise ValueError("Unable to change the status todo which is completed")

        self.status = status
