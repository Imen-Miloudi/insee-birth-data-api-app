from pydantic import BaseModel, ConfigDict
from typing import Literal


class Department(BaseModel):

    model_config = ConfigDict(extra="forbid")

    department: int
    checked: Literal[0, 1] = 0