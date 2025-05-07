from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict


class PostPhotoBase(BaseModel):
    photo_url: str
    group_id: int

class PostPhotoCreate(PostPhotoBase):
    post_id: int

class PostPhotoUpdate(BaseModel):
    photo_url: Optional[str] = None
    group_id: Optional[int] = None

class PostPhotoInDB(PostPhotoBase):
    id: int
    post_id: int

    model_config = ConfigDict(from_attributes=True)


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
    photos: list[PostPhotoInDB]

    class Config:
        from_attributes = True
