# openai

# from pydantic_settings import BaseSettings, SettingsConfigDict 

# class Settings(BaseSettings):
#     openai_api_key: str
#     model_name: str = "gpt-4-turbo-preview"
    
#     model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# settings = Settings()

# Azure OpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_openai_deployment_name: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()