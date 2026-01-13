from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from config import settings
from security import ALGORITHM
from models import User, UserRole, UserStatus

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def http_401():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = http_401()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active (approval pending or blocked).",
        )
    return current_user

def require_roles(*allowed: UserRole):
    async def _checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")
        return current_user
    return _checker

def require_active_and_roles(*allowed: UserRole):
    async def _checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")
        return current_user
    return _checker

def is_admin_like(user: User) -> bool:
    return user.role in {UserRole.SUPERUSER, UserRole.SINDICO_GERAL}

def assert_same_tower_or_admin(actor: User, target_tower_id):
    if is_admin_like(actor):
        return
    if actor.tower_id is None or actor.tower_id != target_tower_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tower scope violation.")
