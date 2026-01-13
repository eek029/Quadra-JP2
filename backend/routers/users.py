from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from database import get_db
from dependencies import get_current_user
from models import User, UserStatus, SignupApprovalRequest, SignupApprovalStatus
from schemas import UserResponse, UserProfileUpdate, SignupApprovalRequestCreate, SignupApprovalRequestResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me/profile", response_model=UserResponse)
async def update_my_profile(payload: UserProfileUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Basic profile fields
    if payload.phone is not None:
        current_user.phone = payload.phone
    if payload.tower_id is not None:
        current_user.tower_id = payload.tower_id
    if payload.unit_number is not None:
        current_user.unit_number = payload.unit_number.strip()
    if payload.birth_date is not None:
        current_user.birth_date = payload.birth_date

    # If user is pending and has enough info, keep pending but allow approval request
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/me/approval-request", response_model=SignupApprovalRequestResponse)
async def create_or_update_approval_request(payload: SignupApprovalRequestCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not payload.unit_number.strip():
        raise HTTPException(status_code=400, detail="unit_number is required")

    # user must have birth_date to be evaluated for 18+, but we can still accept request
    # Update user tower/unit to match request
    current_user.tower_id = payload.tower_id
    current_user.unit_number = payload.unit_number.strip()

    # Find existing pending request
    res = await db.execute(
        select(SignupApprovalRequest).where(
            SignupApprovalRequest.applicant_user_id == current_user.id,
            SignupApprovalRequest.status == SignupApprovalStatus.PENDING,
        )
    )
    req = res.scalars().first()
    if req:
        req.tower_id = payload.tower_id
        req.unit_number = payload.unit_number.strip()
        req.created_at = datetime.utcnow()
    else:
        req = SignupApprovalRequest(
            applicant_user_id=current_user.id,
            tower_id=payload.tower_id,
            unit_number=payload.unit_number.strip(),
            status=SignupApprovalStatus.PENDING,
        )
        db.add(req)

    current_user.status = UserStatus.PENDING
    await db.commit()
    await db.refresh(req)
    return req
