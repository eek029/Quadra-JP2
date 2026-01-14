import asyncio
import asyncpg
import ssl
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL must be set")

    # Replace with asyncpg driver if needed
    if DATABASE_URL.startswith("postgresql+asyncpg://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)

    # Configure SSL
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    # Fallback for self-signed certificates in Supabase pooler
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        # Connect using asyncpg directly
        conn = await asyncpg.connect(
            DATABASE_URL,
            ssl=ssl_context,
            statement_cache_size=0,
        )
        # Execute a simple query
        result = await conn.fetchval("SELECT version()")
        print("Connection successful!")
        print("PostgreSQL version:", result)
        await conn.close()
        print("OK")
    except Exception as e:
        print("Connection failed:", str(e))
        raise

if __name__ == "__main__":
    asyncio.run(test_connection())