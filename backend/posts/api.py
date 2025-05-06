from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Post, Group, UserRoles
from .schemas import PostCreate, PostUpdate, PostRead
from users.schemas import UserRead
from models import get_db
from users.depends import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostRead)
async def create_post(
    post_in: PostCreate,
    user: Annotated[UserRead, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Group).where(Group.id == post_in.group_id))
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if group.group_owner_id != user.id:
        raise HTTPException(status_code=403, detail="Only group owner can create posts")

    post = Post(**post_in.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

@router.get("/", response_model=List[PostRead])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    return result.scalars().all()


@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    user: Annotated[UserRead, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Проверка владельца группы
    group = await db.get(Group, post.group_id)
    if group.group_owner_id != user.id:
        raise HTTPException(status_code=403, detail="Only group owner can update posts")

    for field, value in post_in.model_dump(exclude_none=True).items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post)
    return post


@router.delete("/{post_id}", response_model=bool)
async def delete_post(
    post_id: int,
    user: Annotated[UserRead, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    group = await db.get(Group, post.group_id)
    if group.group_owner_id != user.id or user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=403, detail="Only group owner can delete posts")

    await db.delete(post)
    await db.commit()
    return True
