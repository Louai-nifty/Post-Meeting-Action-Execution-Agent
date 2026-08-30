from pydantic.v1 import NoneStrBytes
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class AgentState(BaseModel):
    