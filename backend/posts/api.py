from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Post, Group, UserRoles, User, PostPhoto
from models import get_db
from users.depends import get_current_user
from users.schemas import UserRead
from .schemas import PostCreate, PostUpdate, PostRead, PostPhotoCreate, PostPhotoUpdate, PostPhotoInDB

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
    refresh_post = (await db.execute(
        select(Post).where(Post.id == post.id).options(selectinload(Post.photos)))).scalar_one_or_none()
    return PostRead(
        author=user.username,
        id=refresh_post.id,
        title=refresh_post.title,
        text=refresh_post.text,
        group_id=refresh_post.group_id,
        created_at=refresh_post.created_at,
        photos=refresh_post.photos,
    )

@router.get("/", response_model=List[PostRead])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post, Group, User)
        .join(Group, Group.id == Post.group_id)
        .join(User, User.id == Group.group_owner_id)
        .options(selectinload(Post.photos))
    )
    rows = result.all()
    posts = [
        PostRead(
            id=post.id,
            title=post.title,
            text=post.text,
            group_id=post.group_id,
            created_at=post.created_at,
            author=post.group.group_owner.username,
            photos=post.photos,
        )
        for post, group, user in rows
    ]
    return posts

@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post, Group, User)
        .join(Group, Group.id == Post.group_id)
        .join(User, User.id == Group.group_owner_id)
        .where(Post.id == post_id)
        .options(selectinload(Post.photos))
    )
    post = result.one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostRead(
        id=post[0].id,
        title=post[0].title,
        text=post[0].text,
        group_id=post[0].group_id,
        created_at=post[0].created_at,
        author=post[0].group.group_owner.username,
        photos=post[0].photos,
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
    refresh_post = await db.execute(select(Post).where(Post.id == post.id).options(selectinload(Post.photos)))
    return refresh_post


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

    if group.group_owner_id != user.id and user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=403, detail="Only group owner can delete posts")

    await db.delete(post)
    await db.commit()
    return True


@router.post("/photo", response_model=PostPhotoInDB)
async def create_post_photo(
        data: PostPhotoCreate,
        user: Annotated[UserRead, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db),
):
    group = await db.get(Group, data.group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    if group.group_owner_id != user.id and user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=403, detail="Нет прав на добавление фото в эту группу")

    post_photo = PostPhoto(**data.model_dump())
    db.add(post_photo)
    await db.commit()
    await db.refresh(post_photo)
    return post_photo


@router.get("/photo", response_model=List[PostPhotoInDB])
async def list_post_photos(
        group_id: int | None = None,
        db: AsyncSession = Depends(get_db),
):
    query = select(PostPhoto)
    if group_id:
        query = query.where(PostPhoto.group_id == group_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.put("/{photo_id}/photo", response_model=PostPhotoInDB)
async def update_post_photo(
        photo_id: int,
        data: PostPhotoUpdate,
        user: Annotated[UserRead, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(PostPhoto).where(PostPhoto.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Фото не найдено")

    group = await db.get(Group, photo.group_id)
    if not group or (group.group_owner_id != user.id and user.role != UserRoles.ADMIN):
        raise HTTPException(status_code=403, detail="Нет прав на редактирование этого фото")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(photo, key, value)

    await db.commit()
    await db.refresh(photo)
    return photo


@router.delete("/{photo_id}/photo", response_model=bool)
async def delete_post_photo(
        photo_id: int,
        user: Annotated[UserRead, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(PostPhoto).where(PostPhoto.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Фото не найдено")

    group = await db.get(Group, photo.group_id)
    if not group or (group.group_owner_id != user.id and user.role != UserRoles.ADMIN):
        raise HTTPException(status_code=403, detail="Нет прав на удаление этого фото")

    await db.delete(photo)
    await db.commit()
    return True
