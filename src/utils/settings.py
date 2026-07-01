from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine
class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_EMAIL:str
    ADMIN_PASSWORD:str



    
    SECRET_KEY : str



    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str


    model_config= SettingsConfigDict(env_file=".env",extra='ignore')
    
   
    
settings = Settings() 


engine = create_async_engine(settings.DATABASE_URL)