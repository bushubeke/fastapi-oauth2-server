#########################################################################
# This is snnipets of codes that might become handy during development
# do not have anything to do the package
#########################################################################
import os
#import asyncio
#print(os.getcwd)
from fastapi import FastAPI,WebSocket,Request,HTTPException
from fastapi.staticfiles import StaticFiles
from .fastapi_curd.curd import sqlalchemycurd
from .models import async_session,engine
from .models.auth_models import Role,RoleModel,User,UserModel

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sqlcurd=sqlalchemycurd()
def create_dev_app():
    app=FastAPI()
    sqlcurd.init_app(app,engine)
    
    modlist=[[User,UserModel],[Role,RoleModel]]
    #modlist=[[Role,RoleModel]]
    sqlcurd.add_curd(modlist)
    #sqlcurd.add_curd(Role,RoleModel)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    @app.get("/")
    def index():
        return {"Message":"You should make your own index page"}

    return app


def create_prod_app():
    app=FastAPI()
    
    app.mount("/static", StaticFiles(directory="/app/static"), name="static")
    
 
    return app

########################################################################

from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List



class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = "YourUsername",
    MAIL_PASSWORD = "strong_password",
    MAIL_FROM = "your@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "your mail server",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

app = FastAPI()


html = """
<p>Thanks for using Fastapi-mail</p> 
"""


@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})    


########################################################################

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()


###########################################################################
import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa

metadata = sa.MetaData()

tbl = sa.Table('tbl', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('val', sa.String(255)))

async def create_table(engine):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS tbl')
        await conn.execute('''CREATE TABLE tbl (
                                  id serial PRIMARY KEY,
                                  val varchar(255))''')

async def go():
    async with create_engine(user='aiopg',
                             database='aiopg',
                             host='127.0.0.1',
                             password='passwd') as engine:

        async with engine.acquire() as conn:
            await conn.execute(tbl.insert().values(val='abc'))

            async for row in conn.execute(tbl.select()):
                print(row.id, row.val)

loop = asyncio.get_event_loop()
loop.run_until_complete(go())

###########################################################################
# this is aiopg version normally, stick to the one above
import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa

metadata = sa.MetaData()

tbl = sa.Table('tbl', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('val', sa.String(255)))

async def create_table(engine):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS tbl')
        await conn.execute('''CREATE TABLE tbl (
                                  id serial PRIMARY KEY,
                                  val varchar(255))''')

async def go():
    async with create_engine(user='aiopg',
                             database='aiopg',
                             host='127.0.0.1',
                             password='passwd') as engine:

        async with engine.acquire() as conn:
            await conn.execute(tbl.insert().values(val='abc'))

            async for row in conn.execute(tbl.select()):
                print(row.id, row.val)

loop = asyncio.get_event_loop()
loop.run_until_complete(go())

###########################################################################

##############################################################################
# postgresql dialect syntax
#############################################################################
# class Document(Base):

#     __tablename__ = 'document'

#     id = Column(Integer, primary_key=True)
#     config = Column(MutableDict.as_mutable(JSON))

#############################################
# this is for nested mutable 
# from sqlalchemy_json import mutable_json_type

# class Document(Base):

#     __tablename__ = 'document'

#     id = Column(Integer, primary_key=True)
#     config = Column(mutable_json_type(dbtype=JSONB, nested=True))
################################################################
# from sqlalchemy.dialects.postgresql import UUID

# id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


######################################################## 
   
# from sqlalchemy.dialects.postgresql import ENUM

# person = Table('user_profile', metadata,
#     name=Column(String(20)),
#     gender=Column(ENUM('female', 'male'))
# );
###################################################

# from sqlalchemy.dialects.postgresql import ARRAY
# number=Column(ARRAY(Integer))




#asyncio.run(async_main())
#Base.metadata.create_all(bind=syncengine)
#Base.metadata.drop_all(bind=syncengine)

# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
    
# from sqlalchemy.ext.asyncio import create_async_engine
# engine = create_async_engine("postgresql+asyncpg://user:pass@hostname/dbname")



#############################################################################
# for sample
#############################################################################
# import asyncio

# from sqlalchemy.ext.asyncio import create_async_engine

# async def async_main():
#     engine = create_async_engine(
#         "postgresql+asyncpg://scott:tiger@localhost/test", echo=True,
#     )

#     async with engine.begin() as conn:
#         await conn.run_sync(meta.drop_all)
#         await conn.run_sync(meta.create_all)

#         await conn.execute(
#             t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}]
#         )

#     async with engine.connect() as conn:

#         # select a Result, which will be delivered with buffered
#         # results
#         result = await conn.execute(select(t1).where(t1.c.name == "some name 1"))

#         print(result.fetchall())

#     # for AsyncEngine created in function scope, close and
#     # clean-up pooled connections
#     await engine.dispose()

# asyncio.run(async_main())

#############################################################################


import typer

from fastapi_migrations.cli import MigrationsCli
import app.cli.action as action

# main cli app
app: typer.Typer = typer.Typer()

# these are our cli actions
app.add_typer(action.app, name='action', help='Common actions the app do')

# this line adds the fastapi-migrations cli commands to our app
app.add_typer(MigrationsCli())

##############################################################################

import typer
from fastapi_migrations import MigrationsConfig, Migrations

app: typer.Typer = typer.Typer()

@app.command()
def show() -> None:
    config = MigrationsConfig()

    migrations = Migrations(config)

    migrations.show()

    
# token=generate_token(data=data,key=key,exp=exp)
#data = jwt.decode(token, app.config['SECRET_KEY'],algorithms="HS256")

####################################################################################################
#this section generates token 
####################################################################################################
def generate_token(data,key,exp):
    return  jwt.encode({'data':data,'exp':exp},key,algorithm="HS256")
def token_decode(data,key):
    return jwt.decode(data,key,algorithms="HS256")
from passlib.hash import pbkdf2_sha512
pbkdf2_sha512.verify(form.data['password'],user.password)
pbkdf2_sha512.using(rounds=25000,salt_size=80).hash(form.data['password'])

# this is how to set expiration time for exp
#  exp=datetime.datetime.utcnow()+datetime.timedelta(hours=5) 

#####################################################################


if data.get("password") is not None:
                        
                        data["password"]=pbkdf2_sha512.using(rounds=25000,salt_size=80).hash(data['password'])
                   try:
                        #print("3 \n")
                        db_model_value=current_sql_model(**data)
                        #print("4 \n")
                        session.add(db_model_value)
                        await session.commit()
                        #session.refresh(db_model_value)
                        #print("5 \n")
                        
                   except Exception as e :
                         #print("6 \n")
                         print(e)
                         await session.rollback()
                         #print("7 \n")
                        
                   finally: 
                         #print("8 \n")
                         await session.close()
                         #print("9 \n")
                   #print("10 \n")
                   return data
              return post_response

##########################################################################
# curl -X 'PUT'  'http://192.168.10.9:5000/user/d9bc7695-82c8-4ef5-8011-314117c38a92'  -H 'accept: application/json'
          # curl -X 'PUT'  'http://192.168.10.9:5000/d9bc7695-82c8-4ef5-8011-314117c38a92' -H 'accept: application/json' -H 'Content-Type: application/json'  -d '{
          # "email": "beimdegefu@yahoo.com", "username": "bushubeke",  "first_name": "Beimnet",  "middle_name": "Bekele",  
          # "last_name": "Degefu",  "password": "bushu1234","active": true}'

{
  "email": "bushu@example.com",
  "username": "Essey",
  "first_name": "Essey",
  "middle_name": "Bekele",
  "last_name": "Degefu",
  "password": "bushu1234",
  "active": true
}


                try:
                    await session.execute(delete(current_sql_model).where(current_sql_model.id==item_uuid)
                    await session.commit()
                    return  { f"Message" : f"sucessfully deleted object "}
                except Exception as e:
                    print(e)
                    await session.rollback()
                    return  { f"Message" : f"sucessfully deleted object "}
                finally:
                    await session.close() 


[
  {
    "email": "beimdegefu@gmail.com",
    "username": "bushu",
    "middle_name": "Bekele",
    "password": "bushu1234",
    "confirmed_at": null,
    "first_name": "Beimnet",
    "id": "5990b908-1174-4581-913f-7f9128c5c888",
    "last_name": "Degefu",
    "date_registerd": "2021-11-05T11:16:29.348583+00:00",
    "active": true
  },
  {
    "email": "beimdegefu@yahoo.com",
    "username": "bushubeke",
    "middle_name": "Bekele",
    "password": "bushu1234",
    "confirmed_at": null,
    "first_name": "Beimnet",
    "id": "e54bb2db-588c-4b88-b035-1d160c8b7daa",
    "last_name": "Degefu",
    "date_registerd": "2021-11-05T11:16:49.968890+00:00",
    "active": true
  },
  {
    "email": "amlakawit@gmail.com",
    "username": "mititi",
    "middle_name": "Bekele",
    "password": "bushu12345",
    "confirmed_at": null,
    "first_name": "Amlakawit",
    "id": "f0d17873-051b-4da8-bd7d-049755f5f6f3",
    "last_name": "Degefu",
    "date_registerd": "2021-11-05T14:28:08.612417+00:00",
    "active": true
  }
]


POST /token HTTP/1.1
Host: as.example.com
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/json

{
    "grant_type": "authorization_code",
    "code": "SplxlOBeZQQYbYS6WxSbIA",
    "redirect_uri": "https://client.example.com/cb"
}

POST /token HTTP/1.1
Host: as.example.com
Content-Type: application/json

{
    "grant_type": "refresh_token",
    "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
    "client_id": "s6BhdRkqt3",
    "client_secret": "7Fjfp0ZBr1KtDRbnfVdmIw",
    "scope": [ "read", "write" ]
}


raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

 raise HTTPException(status_code=400, detail="Incorrect username or password")
 
 
 
 {
  "email": "someone@gmail.com",
  "username": "superspecial",
  "first_name": "Super",
  "middle_name": "User",
  "last_name": "Account",
  "password": "password",
  "disabled": false,
  
}
 
 {
  "email": "bushubekele@example.com",
  "username": "bushu",
  "first_name": "Beimnet",
  "middle_name": "Bekele",
  "last_name": "Degefu",
  "password": "test1234",
  "disabled": false,
  "roles": [
    {
      "name": "superuser",
      "description": "Have access to everything"
    }
  ]
}
 
 
from sqlalchemy import select,update,delete
async def get_user_main():
    #engine = create_async_engine(DATABASE_URL, future=True, echo=True)
    
    async with sessionmade() as session:
            return await session.execute(select(User))
    

  {
    "id": 1,
    "name": "superuser",
    "description": "Have Access to Everything"
  },
  {
    "id": 2,
    "name": "standard",
    "description": "Have Access to Limited resources"
  },
  {
    "id": 3,
    "name": "specfic",
    "description": "Have Access to specified resources"
  }
import asyncio
from oauth2.models import *
loop=asyncio.get_event_loop()
res=loop.run_until_complete(get_user_main())
res=res.scalars().all()
    
    res=select(User).options(joinedload(User.roles))
    from sqlalchemy.dialects import postgresql
    print(str(stmt.compile(dialect=postgresql.dialect())))

#this is the real joined load statment needed
select(User).options(joinedload(User.roles))
res=res.unique().scalars().all()

select(User).where(User.id=1).options(joinedload(User.roles))
res=res.unique().scalars().all()


class OAuth2AuthorizationCodeBearer(OAuth2):
    def __init__(
        self,
        authorizationUrl: str,
        tokenUrl: str,
        refreshUrl: Optional[str] = None,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    )