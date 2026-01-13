from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, date
from database import get_db
from dependencies import require_active_and_roles, assert_same_tower_or_admin
from models import (
    User, UserRole, UserStatus,
    SignupApprovalRequest, SignupApprovalStatus,
)
from schemas import SignupApprovalRequestResponse

router = APIRouter(prefix="/approvals", tags=["approvals"])

def _age_years(birth_date: datetime | None) -> int | None:
    if not birth_date:
        return None
    bd = birth_date.date()
    today = date.today()
    years = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    return years

@router.get("/pending", response_model=list[SignupApprovalRequestResponse])
async def list_pending(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_and_roles(UserRole.PORTEIRO, UserRole.SUBSINDICO, UserRole.SINDICO_GERAL, UserRole.SUPERUSER))):
    q = select(SignupApprovalRequest).where(SignupApprovalRequest.status == SignupApprovalStatus.PENDING)
    # tower scoping for porteiro/subsíndico
    if current_user.role in {UserRole.PORTEIRO, UserRole.SUBSINDICO}:
        if not current_user.tower_id:
            return []
        q = q.where(SignupApprovalRequest.tower_id == current_user.tower_id)
    res = await db.execute(q.order_by(SignupApprovalRequest.created_at.asc()))
    return list(res.scalars().all())

@router.post("/{request_id}/approve", response_model=SignupApprovalRequestResponse)
async def approve_request(request_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_and_roles(UserRole.PORTEIRO, UserRole.SUBSINDICO, UserRole.SINDICO_GERAL, UserRole.SUPERUSER))):
    res = await db.execute(select(SignupApprovalRequest).where(SignupApprovalRequest.id == request_id))
    req = res.scalars().first()
    if not req:
        raise HTTPException(status_code=404, detail="Approval request not found")

    # enforce tower scope
    assert_same_tower_or_admin(current_user, req.tower_id)

    # load applicant
    res = await db.execute(select(User).where(User.id == req.applicant_user_id))
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Applicant user not found")

    # Must be 18+
    age = _age_years(user.birth_date)
    if age is None:
        raise HTTPException(status_code=400, detail="Applicant must set birth_date before approval")
    if age < 18:
        raise HTTPException(status_code=400, detail="Applicant must be 18+ to reserve the court")

    user.status = UserStatus.ACTIVE
    user.is_verified = True
    # default role stays MORADOR unless promoted by admin

    req.status = SignupApprovalStatus.APPROVED
    req.approved_by_user_id = current_user.id
    req.decided_at = datetime.utcnow()

    await db.commit()
    await db.refresh(req)
    return req

@router.post("/{request_id}/reject", response_model=SignupApprovalRequestResponse)
async def reject_request(request_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_and_roles(UserRole.PORTEIRO, UserRole.SUBSINDICO, UserRole.SINDICO_GERAL, UserRole.SUPERUSER))):
    res = await db.execute(select(SignupApprovalRequest).where(SignupApprovalRequest.id == request_id))
    req = res.scalars().first()
    if not req:
        raise HTTPException(status_code=404, detail="Approval request not found")

    assert_same_tower_or_admin(current_user, req.tower_id)

    req.status = SignupApprovalStatus.REJECTED
    req.approved_by_user_id = current_user.id
    req.decided_at = datetime.utcnow()
    await db.commit()
    await db.refresh(req)
    return req
