from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "postgresql://chatbot_user:chatbot_password@localhost:5432/chatbot_db"
    )
    openai_api_key: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


def get_settings():
    return Settings()
