from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Group, UserGroup, User, Post
from models import get_db
from posts.schemas import PostRead
from users.depends import get_current_user
from users.schemas import UserRead
from .schemas import GroupCreate, GroupUpdate, GroupRead

router = APIRouter(prefix="/api/groups", tags=["Groups"])


@router.post("/", response_model=GroupRead)
async def create_group(
    group_in: GroupCreate,
    user: Annotated[UserRead, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    # Создаём группу с текущим пользователем как владельцем
    group = Group(group_owner_id=user.id, **group_in.model_dump())
    db.add(group)
    await db.commit()
    await db.refresh(group)

    # Добавляем пользователя в участники этой группы
    user_group = UserGroup(user_id=user.id, group_id=group.id)
    db.add(user_group)
    await db.commit()

    return group



@router.get("/", response_model=List[GroupRead])
async def get_groups(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Group).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{group_id}", response_model=GroupRead)
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.put("/{group_id}", response_model=GroupRead)
async def update_group(
        user: Annotated[UserRead, Depends(get_current_user)],
        group_id: int,
        group_in: GroupUpdate,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group.group_owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this group")

    for field, value in group_in.model_dump(exclude_none=True).items():
        setattr(group, field, value)

    await db.commit()
    await db.refresh(group)
    return group


@router.delete("/{group_id}", response_model=bool)
async def delete_group(
        group_id: int,
        user: Annotated[UserRead, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group.group_owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this group")

    await db.delete(group)
    await db.commit()
    return True


@router.get("/{group_id}/join", response_model=bool)
async def join_group(
        group_id: int,
        user: Annotated[UserRead, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)
):
    # Проверяем, существует ли группа
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Проверяем, не состоит ли пользователь уже в этой группе
    result = await db.execute(
        select(UserGroup).where(
            UserGroup.group_id == group_id,
            UserGroup.user_id == user.id
        )
    )
    user_group = result.scalar_one_or_none()
    if user_group:
        raise HTTPException(status_code=400, detail="User already in group")

    # Добавляем в группу
    new_user_group = UserGroup(user_id=user.id, group_id=group_id)
    db.add(new_user_group)
    await db.commit()
    return True

@router.get("/{group_id}/members", response_model=List[UserRead])
async def get_group_members(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).join(UserGroup).where(UserGroup.group_id == group_id)
    )
    return result.scalars().all()


@router.delete("/{group_id}/leave", response_model=bool)
async def leave_group(
    group_id: int,
    user: Annotated[UserRead, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserGroup).where(
            UserGroup.group_id == group_id,
            UserGroup.user_id == user.id
        )
    )
    user_group = result.scalar_one_or_none()

    if not user_group:
        raise HTTPException(status_code=404, detail="You are not a member of this group")

    await db.delete(user_group)
    await db.commit()
    return True


@router.get("/{group_id}/posts", response_model=List[PostRead])
async def get_group_posts(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Post, Group, User)
        .join(Group, Group.id == Post.group_id)
        .join(User, User.id == Group.group_owner_id)
        .options(selectinload(Post.photos))
        .where(Post.group_id == group_id)
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


@router.get("/{group_id}/is-member/")
async def user_is_member(
        user: Annotated[UserRead, Depends(get_current_user)],
        group_id: int,
        session: Annotated[AsyncSession, Depends(get_db)]
):
    # Загружаем пользователя с его группами
    result = await session.execute(
        select(User).where(User.id == user.id).options(selectinload(User.groups))
    )
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Проверяем, состоит ли в группе
    is_member = any(group.id == group_id for group in db_user.groups)

    return {"is_member": is_member}
