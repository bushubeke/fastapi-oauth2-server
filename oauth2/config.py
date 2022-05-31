import os

# from typing import Any, Dict, List, Optional, Union

# from boto.s3.connection import S3Connection
# # s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'],os.environ['S3_SECRET'])
# s3 = S3Connection(os.environ("SECRET_KEY"), os.environ("DATABASE_ASYNC_URI"),os.environ('DATABASE_MIGRATION_URI') )
# print(s3)
# print(dir(s3))

from pydantic import BaseSettings 


class Settings(BaseSettings):
    #email settings to be filled
    # SMTP_TLS: bool = True
    # SMTP_PORT: Optional[int] = None
    # SMTP_HOST: Optional[str] = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None
    # EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    # EMAILS_FROM_NAME: Optional[str] = None

    # database settings
    # DATABASE_MIGRATION_URI = 'postgresql+psycopg2://postgres:something@192.168.10.5:5432/development-template'
    # DATABASE_ASYNC_URI='postgresql+asyncpg://postgres:something@192.168.10.5:5432/development-template'
    DATABASE_MIGRATION_URI : str=os.getenv('DATABASE_MIGRATION_URI') 
    DATABASE_ASYNC_URI : str=os.getenv("DATABASE_ASYNC_URI")
    SECRET_KEY : str = os.getenv("SECRET_KEY")
    class Config:
        # case_sensitive = True
        env_file = ".env"

settings = Settings()