from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dependencies import get_db, get_current_user
from models import User, UserStatus, UserRole
from schemas import UserResponse
from config import settings
from security import create_access_token
from datetime import timedelta
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.OAUTH_REDIRECT_URI}&scope=openid%20email%20profile"
    }

@router.get("/callback/google")
async def callback_google(code: str, db: AsyncSession = Depends(get_db)):
    # Exchange code for token
    async with httpx.AsyncClient() as client:
        token_res = await client.post("https://oauth2.googleapis.com/token", data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.OAUTH_REDIRECT_URI,
            "grant_type": "authorization_code"
        })
        token_data = token_res.json()
        
        if "id_token" not in token_data:
             raise HTTPException(status_code=400, detail="Invalid code or google error")
             
        # Get user info
        user_res = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={
            "Authorization": f"Bearer {token_data['access_token']}"
        })
        user_info = user_res.json()
        
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="No email found in google profile")
        
    # Check if user exists
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    if not user:
        # Create new user
        # Note: In a real app we might want to restrict to approved emails or default to pending
        user = User(
            email=email,
            name=user_info.get("name", "Unknown"),
            auth_provider="google",
            role=UserRole.MORADOR,
            status=UserStatus.PENDING,
            is_verified=False,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    # Create JWT
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(seconds=settings.JWT_EXPIRES_IN)
    )
    
    # Redirect to frontend with token
    from fastapi.responses import RedirectResponse
    frontend_url = settings.CORS_ORIGINS.split(",")[0] # Assumes first origin is frontend
    return RedirectResponse(url=f"{frontend_url}/auth/callback?token={access_token}")

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
