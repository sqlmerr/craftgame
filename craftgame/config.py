from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseModel):
    password: str = "password"
    user: str = "postgres"
    port: int = 5432
    db: str = ""
    host: str = "0.0.0.0"

    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    ai_token: str
    bot_token: str
    jwt_secret: str

    postgres: PostgresConfig = PostgresConfig()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
