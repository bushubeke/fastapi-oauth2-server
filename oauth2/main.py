import uvicorn
from fastapi import FastAPI,Depends

from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from .approutes import apirouter


def create_dev_app():
    app=FastAPI()
   
    
    origins = [ "*"]
    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )
    
    app.include_router(apirouter,prefix="/admin")
    
    templates = Jinja2Templates(directory="templates")
    
    
    @app.get("/")
    def index():
        return {"Message":"You should make your own index page"}
    
    return app

def create_testing_app():
    app=FastAPI()
   
    
    origins = [ "*"]
    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )
    
    app.include_router(apirouter,prefix="/admin")
    
    templates = Jinja2Templates(directory="templates")
    
    @app.get("/")
    def index():
        return {"Message":"You should make your own index page"}
    
    return uvicorn.run(app, host="0.0.0.0", port=9000, reload=True, log_level="debug", debug=True,
                workers=1, limit_concurrency=1)
def create_prod_app():
    app=FastAPI()
   
    
    origins = [ "*"]
    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )
    
    app.include_router(apirouter,prefix="/admin")
    
    templates = Jinja2Templates(directory="templates")
    
    @app.get("/")
    def index():
        return {"Message":"You should make your own index page"}
    
    return app   
    
     #############################################################3
    # heroku settings 
    #  https://fastapi-oauth2.herokuapp.com/
    #  https://git.heroku.com/fastapi-oauth2.git

    # web: gunicorn manage:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9000 --reload -w 2
    # web: gunicorn -b 0.0.0.0:9000 --reload -w 4 -k uvicorn.workers.UvicornWorker manage:app
    
    
    ##############################################################