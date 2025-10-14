from typing import List, Optional
from dynaconf import Dynaconf
from pydantic import BaseModel, Field


class LogsConfig(BaseModel):
    level_name: str = Field(alias="LEVEL_NAME")
    format: Optional[str] = Field(default=None, alias="FORMAT")


class I18nConfig(BaseModel):
    default_locale: str = Field(alias="default_locale")
    locales: List[str] = Field(alias="locales")


class BotConfig(BaseModel):
    token: str = Field(alias="TOKEN")
    parse_mode: str = Field(alias="PARSE_MODE")


class PostgresConfig(BaseModel):
    name: str = Field(alias="NAME")
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")
    user: str = Field(alias="USER")
    password: str = Field(alias="PASSWORD")


class RedisConfig(BaseModel):
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")
    database: int = Field(alias="DATABASE")
    username: Optional[str] = Field(default=None, alias="USERNAME")
    password: Optional[str] = Field(default=None, alias="PASSWORD")


class NatsConfig(BaseModel):
    servers: str = Field(alias="SERVERS")
    delayed_consumer_subject: str = Field(alias="DELAYED_CONSUMER_SUBJECT")
    delayed_consumer_stream: str = Field(alias="DELAYED_CONSUMER_STREAM")
    delayed_consumer_durable_name: str = Field(alias="DELAYED_CONSUMER_DURABLE_NAME")


class CacheConfig(BaseModel):
    use_cache: bool = Field(alias="USE_CACHE")


class AppConfig(BaseModel):
    logs: LogsConfig
    i18n: I18nConfig
    bot: BotConfig
    postgres: PostgresConfig
    redis: RedisConfig
    nats: NatsConfig
    cache: CacheConfig


# Инициализация Dynaconf
_settings = Dynaconf(
    envvar_prefix=False,  # "DYNACONF",
    environments=True,  # Автоматически использовать секцию текущей среды
    env_switcher="ENV_FOR_DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
)


def get_config() -> AppConfig:
    """
    Возвращает типизированную конфигурацию приложения.
    
    Returns:
        AppConfig: Валидированная Pydantic модель с настройками приложения
    """
    # Создаем модели напрямую из данных Dynaconf
    logs = LogsConfig.model_validate({
        "LEVEL_NAME": _settings.logs.level_name,
        "FORMAT": _settings.logs.format,
    })
    
    i18n = I18nConfig.model_validate({
        "default_locale": _settings.i18n.default_locale,
        "locales": _settings.i18n.locales,
    })
    
    bot = BotConfig.model_validate({
        "TOKEN": _settings.bot_token,
        "PARSE_MODE": _settings.bot.parse_mode,
    })
    
    postgres = PostgresConfig.model_validate({
        "NAME": _settings.postgres.name,
        "HOST": _settings.postgres.host,
        "PORT": _settings.postgres.port,
        "USER": _settings.postgres.user,
        "PASSWORD": _settings.postgres_password,
    })
    
    redis = RedisConfig.model_validate({
        "HOST": _settings.redis.host,
        "PORT": _settings.redis.port,
        "DATABASE": _settings.redis.database,
        "USERNAME": _settings.redis_username,
        "PASSWORD": _settings.redis_password,
    })
    
    nats = NatsConfig.model_validate({
        "SERVERS": _settings.nats.servers,
        "DELAYED_CONSUMER_SUBJECT": _settings.nats.delayed_consumer_subject,
        "DELAYED_CONSUMER_STREAM": _settings.nats.delayed_consumer_stream,
        "DELAYED_CONSUMER_DURABLE_NAME": _settings.nats.delayed_consumer_durable_name,
    })
    
    cache = CacheConfig.model_validate({
        "USE_CACHE": _settings.cache.use_cache,
    })
    
    return AppConfig(
        logs=logs,
        i18n=i18n,
        bot=bot,
        postgres=postgres,
        redis=redis,
        nats=nats,
        cache=cache,
    )


# Для обратной совместимости оставляем объект settings
settings = _settings
