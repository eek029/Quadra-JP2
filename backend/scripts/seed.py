import asyncio
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import AsyncSessionLocal
from models import Court, User, UserRole, UserStatus
from sqlalchemy import select

async def seed():
    async with AsyncSessionLocal() as session:
        print("Seeding database...")

        # Default court
        result = await session.execute(select(Court))
        court = result.scalars().first()
        if not court:
            print("Creating default Court...")
            court = Court(name="Quadra Poliesportiva", is_active=True)
            session.add(court)
            await session.commit()
            print("Court created.")
        else:
            print("Court already exists.")

        # Ensure SUPERUSER exists (set SUPERUSER_EMAIL in env)
        super_email = os.getenv("SUPERUSER_EMAIL")
        if super_email:
            res_u = await session.execute(select(User).where(User.email == super_email))
            su = res_u.scalars().first()
            if not su:
                print("Creating SUPERUSER...")
                su = User(
                    email=super_email,
                    name="System Admin",
                    auth_provider="seed",
                    role=UserRole.SUPERUSER,
                    status=UserStatus.ACTIVE,
                    is_verified=True,
                )
                session.add(su)
                await session.commit()
                print("SUPERUSER created.")
            else:
                print("SUPERUSER already exists.")
        else:
            print("SUPERUSER_EMAIL not set; skipping superuser seed.")

if __name__ == "__main__":
    asyncio.run(seed())
