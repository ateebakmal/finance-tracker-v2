"""Application settings, loaded from environment variables / the .env file.

Using pydantic-settings means: never hard-code secrets, and every value is
type-validated at startup (a missing DATABASE_URL fails loudly, immediately).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
# TODO: Do i need to change str with SecretStr for import things
from pydantic import SecretStr


class Settings(BaseSettings):
    # Reads from a local .env file; ignores any env vars we don't declare here.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str          # postgresql+asyncpg://user:pass@host/dbname
    db_ssl: str | None = None   # "require" for Neon; None/blank for local Postgres
    db_echo: bool = False       # if True, SQLAlchemy prints every SQL statement

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    frontend_url: str
    
    session_secret:str
    jwt_secret:str
    algorithm: str = "HS256"

    refresh_token_expire_days:int
    access_token_expire_minutes:int

    cookie_secure:bool = False
    cookie_samesite:str = "lax"

# One shared instance imported everywhere: `from config import settings`
# NOTE the () — you must *instantiate* the class, not just reference it.
settings = Settings() #type: ignore[] #Loaded from .env files
