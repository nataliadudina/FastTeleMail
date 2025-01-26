from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DatabaseSettings(BaseSettings):
    # Database settings
    DB_USER: str = Field('postgres', env='DB_USER')
    DB_PASS: str = Field('postgres', env='DB_PASS')
    DB_HOST: str = Field('localhost', env='DB_HOST')
    DB_PORT: int = Field(5432, env='DB_PORT')
    DB_NAME: str = Field('postgres', env='DB_NAME')

    @property
    def uri(self) -> str:
        return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class EmailSettings(BaseSettings):
    # Email settings
    MAIL_FROM: str = Field('', env='EMAIL_USER')
    EMAIL_HOST: str = Field('', env='EMAIL_HOST')
    EMAIL_PORT: int = Field(465, env='EMAIL_PORT')
    EMAIL_USER: str = Field('', env='EMAIL_USER')
    EMAIL_PASSWORD: str = Field('', env='EMAIL_PASSWORD')
    MAIL_STARTTLS: bool = Field(False, env='MAIL_STARTTLS')
    MAIL_SSL_TLS: bool = Field(True, env='MAIL_SSL_TLS')


class RedisSettings(BaseSettings):
    # Redis settings
    REDIS_URL: str = Field('redis://localhost:6379', env='REDIS_URL')


class TelegramSettings(BaseSettings):
    # Telegram API settings
    TELEGRAM_API_TOKEN: str = Field('', env='TELEGRAM_API_TOKEN')
    TELEGRAM_URL: str = Field('https://api.telegram.org/bot', env='TELEGRAM_URL')


class AppSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    email: EmailSettings = EmailSettings()
    redis: RedisSettings = RedisSettings()
    telegram: TelegramSettings = TelegramSettings()
    title: str = 'Notification API'
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')


app_settings = AppSettings()
