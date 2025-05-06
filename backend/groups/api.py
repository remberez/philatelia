from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Group
from models import get_db
from users.depends import get_current_user
from users.schemas import UserRead
from .schemas import GroupCreate, GroupUpdate, GroupRead

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("/", response_model=GroupRead)
async def create_group(
        group_in: GroupCreate,
        user: Annotated[UserRead, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db),
):
    group = Group(group_owner_id=user.id, **group_in.model_dump())
    db.add(group)
    await db.commit()
    await db.refresh(group)
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
