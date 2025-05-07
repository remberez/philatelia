from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import User, UserRoles
from models import get_db
from users.depends import get_current_user
from users.schemas import UserRead, UserUpdate, UserCreate
from users.auth import verify_password, create_access_token, get_password_hash

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_pass):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=UserRead, status_code=201)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(User.email == user.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_pass=get_password_hash(user.password),
        role=UserRoles.USER
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# ✅ Получить себя
@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# ✅ Обновить себя
@router.put("/me", response_model=UserRead)
async def update_me(
        user_update: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    stmt = (
        update(User)
        .where(User.id == current_user.id)
        .values(
            username=user_update.username or current_user.username,
            email=user_update.email or current_user.email,
            hashed_pass=get_password_hash(user_update.password) if user_update.password else current_user.hashed_pass
        )
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()

    result = await db.execute(select(User).where(User.id == current_user.id))
    return result.scalar_one()


# ✅ Удалить себя
@router.delete("/me", status_code=204)
async def delete_me(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    await db.execute(delete(User).where(User.id == current_user.id))
    await db.commit()
