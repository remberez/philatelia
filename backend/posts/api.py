from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Post, Group, UserRoles, User
from .schemas import PostCreate, PostUpdate, PostRead
from users.schemas import UserRead
from models import get_db
from users.depends import get_current_user

router = APIRouter(prefix="/api/posts", tags=["Posts"])

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
    result = await db.execute(
        select(Post, Group, User)  # Запрос на выборку постов, групп и пользователей
        .join(Group, Group.id == Post.group_id)  # Объединяем Post и Group
        .join(User, User.id == Group.group_owner_id)  # Объединяем Group и User (владельца)
    )
    posts = result.all()
    post_list = [
        PostRead(
            id=post.Post.id,
            title=post.Post.title,
            text=post.Post.text,
            group_id=post.Post.group_id,
            created_at=post.Post.created_at,
            author=post.User.username  # username владельца группы
        ) for post in posts
    ]
    return post_list


@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post, Group, User)
        .join(Group, Group.id == Post.group_id)
        .join(User, User.id == Group.group_owner_id)
        .where(Post.id == post_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostRead(
        id=post[0].id,
        title=post[0].title,
        text=post[0].text,
        group_id=post[0].group_id,
        created_at=post[0].created_at,
        author=post[2].username  # username владельца группы
    )


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
