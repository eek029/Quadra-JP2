from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from dependencies import require_active_and_roles, assert_same_tower_or_admin, is_admin_like
from models import User, UserRole
from pydantic import BaseModel
from uuid import UUID

router = APIRouter(prefix="/admin", tags=["admin"])

class RoleUpdate(BaseModel):
    user_id: UUID
    role: UserRole
    tower_id: UUID | None = None

@router.post("/assign-role")
async def assign_role(payload: RoleUpdate, db: AsyncSession = Depends(get_db), actor: User = Depends(require_active_and_roles(UserRole.SUBSINDICO, UserRole.SINDICO_GERAL, UserRole.SUPERUSER))):
    res = await db.execute(select(User).where(User.id == payload.user_id))
    target = res.scalars().first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    if actor.role == UserRole.SUBSINDICO:
        # subsíndico só pode promover porteiro na própria torre
        if payload.role != UserRole.PORTEIRO:
            raise HTTPException(status_code=403, detail="Subsíndico can only assign PORTEIRO")
        if actor.tower_id is None:
            raise HTTPException(status_code=400, detail="Subsíndico must have tower_id")
        if payload.tower_id and payload.tower_id != actor.tower_id:
            raise HTTPException(status_code=403, detail="Tower scope violation")
        assert_same_tower_or_admin(actor, target.tower_id or actor.tower_id)
        target.tower_id = actor.tower_id

    elif actor.role == UserRole.SINDICO_GERAL:
        # síndico geral pode atribuir porteiro/subsíndico/síndico geral
        if payload.role == UserRole.SUPERUSER:
            raise HTTPException(status_code=403, detail="Only SUPERUSER can assign SUPERUSER")
        if payload.tower_id:
            target.tower_id = payload.tower_id

    elif actor.role == UserRole.SUPERUSER:
        if payload.tower_id is not None:
            target.tower_id = payload.tower_id

    target.role = payload.role
    await db.commit()
    return {"ok": True}
