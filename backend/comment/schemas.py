from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    post_id: int

class CommentUpdate(BaseModel):
    text: Optional[str] = None

class CommentInDB(CommentBase):
    id: int
    created_at: datetime
    user_id: int
    post_id: int

    class Config:
        orm_mode = True

class CommentRead(CommentInDB):
    pass
