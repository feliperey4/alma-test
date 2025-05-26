"""
Written by Felipe Rey
"""
import os

DB_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/leads_db")
SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
ATTORNEY_EMAIL: str = os.getenv("ATTORNEY_EMAIL", "attorney@example.com")

# AUTH
AUTH_SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY", "your-secret-key")# base secret key to gen the hashes
AUTH_ALGORITHM: str = os.getenv("AUTH_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))