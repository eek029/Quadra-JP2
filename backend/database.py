from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
import ssl
import certifi
from dotenv import load_dotenv

load_dotenv()

# Get DB URL from env
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure using async driver for AsyncEngine
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL and DATABASE_URL.startswith("postgresql+psycopg2://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set")

# Configure SSL context with certifi for Supabase pooler
ssl_context = ssl.create_default_context(cafile=certifi.where())
# Fallback for self-signed certificates in Supabase pooler
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={
        "ssl": ssl_context,
        "statement_cache_size": 0,  # Disable prepared statements for pgbouncer
    },
)



AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
