import typer
import asyncio
# import uvicorn
import subprocess
from pathlib import Path
from passlib.hash import pbkdf2_sha512
from sqlalchemy.orm import Session

SOURCE_FILE = Path(__file__).resolve()
SOURCE_DIR = SOURCE_FILE.parent

# from fastapi_migrations import MigrationsConfig, Migrations
# from fastapi_migrations.cli import MigrationsCli
# print(SOURCE_DIR)
# from fastapi_sqlalchemy import DBSessionMiddleware
from oauth2.main import create_dev_app
from oauth2.config import settings
from oauth2.models import async_main,droptables, engine,User,Role,RolesUsers


capp = typer.Typer()
app=create_dev_app()

@capp.command()
def create_super():
        try:
            user={
            "email": "someone@gmail.com",
            "username": "superspecial",
            "first_name": "Super",
            "middle_name": "User",
            "last_name": "Account",
            "password": pbkdf2_sha512.using(rounds=25000,salt_size=80).hash("password"),
            "disabled": False
            
            }
            role=  {
                "name": "superuser",
                "description": "Have access to everything"
                }
            userrole={
                "user_id": 1,
                "role_id": 1
                }
            user=User(**user)
            # print(user.asdict())
            role=Role(**role)
            userrole=RolesUsers(**userrole)
            with Session(engine) as session:
                session.add(user)
                session.commit()

                session.add(role)
                session.commit()

                session.add(userrole)
                session.commit()

            

        except Exception as e:
            print(e)
            # db_session.rollback()
            
        
@capp.command()
def upgrade():
    asyncio.run(async_main())
    
@capp.command()
def test():
    subprocess.run(["pytest", "tests","--asyncio-mode=strict"])
@capp.command()
def run():
    subprocess.run(["uvicorn", "manage:app", "--host" ,"0.0.0.0","--port","9000","--reload"])
    
@capp.command()
def rung():
   
    subprocess.run(["gunicorn", "manage:app", "-k" ,"uvicorn.workers.UvicornWorker","-b" ,"0.0.0.0:9000","--reload","-w","1"]) 
@capp.command()
def drop():
    asyncio.run(droptables())

if __name__ == "__main__":
    capp()