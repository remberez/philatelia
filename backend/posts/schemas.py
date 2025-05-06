from datetime import datetime

from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    text: str
    group_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str | None = None
    text: str | None = None

class PostRead(BaseModel):
    id: int
    title: str
    text: str
    group_id: int
    created_at: datetime
    author: str

    class Config:
        orm_mode = True
