from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="sap-ops-mcp", alias="APP_NAME")
    app_env: str = Field(default="dev", alias="APP_ENV")
    app_log_level: str = Field(default="INFO", alias="APP_LOG_LEVEL")

    sap_ashost: str = Field(default="", validation_alias=AliasChoices("SAP_ASHOST", "SAP_RFC_ASHOST"))
    sap_sysnr: str = Field(default="00", validation_alias=AliasChoices("SAP_SYSNR", "SAP_RFC_SYSNR"))
    sap_client: str = Field(default="100", validation_alias=AliasChoices("SAP_CLIENT", "SAP_RFC_CLIENT"))
    sap_user: str = Field(default="", validation_alias=AliasChoices("SAP_USER", "SAP_RFC_USER"))
    sap_passwd: str = Field(default="", validation_alias=AliasChoices("SAP_PASSWD", "SAP_RFC_PASSWD"))
    sap_lang: str = Field(default="EN", validation_alias=AliasChoices("SAP_LANG", "SAP_RFC_LANG"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
