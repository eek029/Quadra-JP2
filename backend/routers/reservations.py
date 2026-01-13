from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from datetime import datetime, timedelta, date
from database import get_db
from dependencies import get_current_active_user, require_active_and_roles, assert_same_tower_or_admin, is_admin_like
from models import User, UserRole, UserStatus, Reservation, ReservationStatus
from schemas import ReservationCreate, ReservationResponse

router = APIRouter(prefix="/reservations", tags=["reservations"])

def _age_ok(user: User) -> bool:
    if not user.birth_date:
        return False
    today = date.today()
    bd = user.birth_date.date()
    years = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    return years >= 18

@router.get("", response_model=list[ReservationResponse])
async def list_reservations(date_str: str | None = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    q = select(Reservation)
    if date_str:
        try:
            d = datetime.fromisoformat(date_str).date()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")
        start = datetime.combine(d, datetime.min.time())
        end = start + timedelta(days=1)
        q = q.where(Reservation.start_time >= start, Reservation.start_time < end)
    q = q.where(Reservation.status != ReservationStatus.CANCELLED).order_by(Reservation.start_time.asc())
    res = await db.execute(q)
    return list(res.scalars().all())

@router.get("/mine", response_model=list[ReservationResponse])
async def my_reservations(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    res = await db.execute(
        select(Reservation).where(Reservation.user_id == current_user.id).order_by(Reservation.start_time.desc())
    )
    return list(res.scalars().all())

@router.post("", response_model=ReservationResponse)
async def create_reservation(payload: ReservationCreate, db: AsyncSession = Depends(get_db), actor: User = Depends(get_current_active_user)):
    # Determine target (who is reserving)
    target_user_id = payload.reserved_for_user_id or actor.id

    if payload.reserved_for_user_id and actor.role == UserRole.MORADOR:
        raise HTTPException(status_code=403, detail="Morador can only reserve for themselves.")

    # Load target user
    res = await db.execute(select(User).where(User.id == target_user_id))
    target = res.scalars().first()
    if not target:
        raise HTTPException(status_code=404, detail="Target user not found")
    if target.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=403, detail="Target user is not active")
    if not _age_ok(target):
        raise HTTPException(status_code=403, detail="Only 18+ can reserve the court")

    # Tower scoping for porteiro/subsíndico
    if actor.role in {UserRole.PORTEIRO, UserRole.SUBSINDICO}:
        assert_same_tower_or_admin(actor, target.tower_id)

    # Validate time window
    if payload.end_time <= payload.start_time:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")
    duration = payload.end_time - payload.start_time
    if duration <= timedelta(0) or duration > timedelta(hours=2):
        # Optional: allow multiple slots, but your rule is 2h/day; single booking could be <=2h
        raise HTTPException(status_code=400, detail="Invalid duration (max 2h per reservation)")

    # 2h/day limit
    day = payload.start_time.date()
    day_start = datetime.combine(day, datetime.min.time())
    day_end = day_start + timedelta(days=1)
    res = await db.execute(
        select(func.coalesce(func.sum(func.extract('epoch', Reservation.end_time - Reservation.start_time)), 0))
        .where(
            Reservation.user_id == target.id,
            Reservation.status != ReservationStatus.CANCELLED,
            Reservation.start_time >= day_start,
            Reservation.start_time < day_end,
        )
    )
    used_seconds = float(res.scalar() or 0)
    if used_seconds + duration.total_seconds() > 2 * 3600:
        raise HTTPException(status_code=400, detail="Daily limit exceeded (max 2h/day)")

    # Overlap check (application-level; you should also add DB constraint)
    overlap_q = select(Reservation).where(
        Reservation.court_id == payload.court_id,
        Reservation.status != ReservationStatus.CANCELLED,
        Reservation.start_time < payload.end_time,
        Reservation.end_time > payload.start_time,
    )
    res = await db.execute(overlap_q)
    if res.scalars().first():
        raise HTTPException(status_code=409, detail="Time slot already reserved")

    r = Reservation(
        court_id=payload.court_id,
        user_id=target.id,
        created_by_user_id=actor.id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        notes=payload.notes,
        status=ReservationStatus.CONFIRMED,
    )
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r

@router.post("/{reservation_id}/cancel", response_model=ReservationResponse)
async def cancel_reservation(reservation_id: str, db: AsyncSession = Depends(get_db), actor: User = Depends(get_current_active_user)):
    res = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    r = res.scalars().first()
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    # Only owner or sindico_geral/superuser can cancel
    if r.user_id != actor.id and actor.role not in {UserRole.SINDICO_GERAL, UserRole.SUPERUSER}:
        raise HTTPException(status_code=403, detail="Insufficient permissions to cancel")
    r.status = ReservationStatus.CANCELLED
    r.cancelled_by = actor.id
    await db.commit()
    await db.refresh(r)
    return r
