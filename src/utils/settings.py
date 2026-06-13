from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine
class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_EMAIL:str
    ADMIN_PASSWORD:str
    model_config= SettingsConfigDict(env_file=".env",extra='ignore')
    
   
    
settings = Settings() 


engine = create_async_engine(settings.DATABASE_URL)