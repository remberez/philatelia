from pydantic import BaseModel
from typing import List, Optional

class GroupBase(BaseModel):
    name: str
    description: str
    groupname: str

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    groupname: Optional[str] = None

class GroupRead(GroupBase):
    id: int

    class Config:
        orm_mode = True
