
import uuid
from fastapi import APIRouter, Depends,HTTPException, status,Request

from  .config import settings
# from  .celeryback import *
from passlib.hash import pbkdf2_sha512
from datetime import datetime , timedelta,timezone
from .models import *
from .utils import *
from sqlalchemy import select,update,delete
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from json import  dumps as jsondumps,load as jsonload,JSONDecoder
import jwt
###########################################################
apirouter = APIRouter()

##########################################################
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    
    user= jwt.decode(token,settings.SECRET_KEY,algorithms="HS256")
    
    user=user["data"]
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user=jsondumps(user)
    
    user=JSONDecoder().decode(user)
   
    return user


async def get_current_active_user(current_user: UserModelLogin=Depends(get_current_user)):
    
    
    if current_user["disabled"] is True :
        raise HTTPException(status_code=400, detail="Inactive user")
   
    return current_user

##########################################################
##########################################################
@apirouter.post("/user/register")
async def register_user(request : Request,user : UserModel,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
    
    available_roles=[x["name"] for x in current_user["roles"]]
    if len([x for x in available_roles if x in User.roles_required()])>0: 
        try:
            data=dict(user)
            data=dataclass_to_dic(data)
            data['password']=pbkdf2_sha512.using(rounds=25000,salt_size=80).hash(data['password'])
            
            user=User(**data)
            
            session.add(user)
            await session.commit()
            return {"Message":"insert has been sucessful"} 
        except Exception as e:
            await session.rollback()
            print(e)
            raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
        finally:
        
            await session.close()
    else:
        raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")
@apirouter.get("/user/{item_uuid}",response_model=UserModel)
async def get_user(request : Request,item_uuid :uuid.UUID,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            # response_model=UserModel
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in User.roles_required()])>0:
                try:
                    #this is the real joined load statment needed
                    # select(User).options(joinedload(User.roles))
                    user=await session.execute(select(User).where(User.uid==item_uuid).options(joinedload(User.roles)))
                    user=user.unique().scalars().first()
                    
                    return UserModel.parse_obj(user.asdict())
                except Exception as e:
                    print(e)
                    raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
                    
                finally:
                    await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")
@apirouter.get("/users/all",response_model=List[UserModelAll] )
async def get_all_users(request : Request,session : AsyncSession=Depends(get_session),current_user :UserModelLogin = Depends(get_current_active_user)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in User.roles_required()])>0:    
                try:
                    
                    #this is the real joined load statment needed
                    # select(User).options(joinedload(User.roles))
                    users= await session.execute(select(User).options(joinedload(User.roles)))
                   
                    users=users.unique().scalars().all()
                    
                    return [UserModelAll.parse_obj(x.asdict()) for x in users]
                except Exception as e:
                    print(e)
                    await session.rollback()
                    raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
                finally:
                    await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")

@apirouter.put("/userrole/{item_uuid}")
async def update_user(request : Request,user : UserModel,item_uuid :uuid.UUID,session : AsyncSession=Depends(get_session),current_user :UserModelLogin = Depends(get_current_active_user)):
            
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in User.roles_required()])>0:  
                data=dict(user)
                if data.get('password',None):
                    data['password']=pbkdf2_sha512.using(rounds=25000,salt_size=80).hash(data['password'])
                data=dataclass_to_dic(data)
                try:
                    await session.execute(update(User).where(User.id ==item_uuid).values(**data))       
                
                    await session.commit()
                    return { f"Message" : f"sucessfully updated object "}
                except Exception as e:
                    print(e)
                    await session.rollback()
                    raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
                finally:
                    await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")
@apirouter.delete("/user/{item_uuid}")
async def delete_user(request : Request,item_uuid :uuid.UUID ,session : AsyncSession=Depends(get_session),current_user :UserModelLogin = Depends(get_current_active_user)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in User.roles_required()])>0:        
                    try:
                    
                         await session.execute(delete(User).where(User.uid == item_uuid))
                         await session.commit()
                         return {"Message" :"Sucessfully Deleted object"}
                    except Exception as e:
                         await session.rollback()
                         raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
     
                    finally:
                         await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")
                
                    
@apirouter.delete("/user/all")
async def delete_all_user(request : Request,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in User.roles_required()])>0:
                    try:
                    
                         await session.execute(delete(User))
                         await session.commit()
                         return {"Message" :"Sucessfully Deleted Rows"}
                    except Exception as e:
                         
                         await session.rollback()
                         raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
     
                    finally:
                         await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")

######################################################

######################################################

@apirouter.post("/role/register")
async def register_roles(request : Request,role : RoleModel,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in Role.roles_required()])>0:
                try:
                    data=dict(role)
                    data=dataclass_to_dic(data)
                    
                    role=Role(**data)
                    
                    session.add(role)
                    await session.commit()
                    return {"Message":"insert has been sucessful"} 
                except Exception as e:
                    await session.rollback()
                    raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
                    
                finally:
                    
                    await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")


@apirouter.get("/role/{item_id}",response_model=RoleModelAll)
async def get_role(request : Request,item_id :int = None,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in Role.roles_required()])>0:
                try:
                    role=await session.execute(select(Role).filter_by(id=item_id))
                    role=role.scalars().first()
                
                    return RoleModelAll.parse_obj(role.asdict())
                except Exception as e:
                    print(e)
                    raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
                    
                finally:
                    await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")

@apirouter.get("/roles/all",response_model=List[RoleModelAll])
async def get_all_roles(request : Request,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in Role.roles_required()])>0:
                try:
                #  print('###1')
                    roles= await session.execute(select(Role))
                    roles=roles.scalars().all()
                
                #  print('###2')
                    return [RoleModelAll.parse_obj(x.asdict()) for x in roles] 
                except Exception as e:
                    print(e)
                    await session.rollback()
                    raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
                finally:
                    await session.close()

            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")



@apirouter.put("/roleupdate/{item_id}")
async def update_role(request : Request,role : RoleModelAll,item_id :int,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in Role.roles_required()])>0:
                data=dict(role)
                data=dataclass_to_dic(data)
                try:
                    
                    await session.execute(update(Role).where(Role.id ==item_id).values(**data))
                    # print("####3")
                    await session.commit()
                    return { f"Message" : f"sucessfully updated object "}
                except Exception as e:
                    print(e)
                    await session.rollback()
                    raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
                finally:
                    await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")


@apirouter.delete("/role/{item_id}")
async def delete_role(request : Request,item_id :int ,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in Role.roles_required()])>0:
                try:
                
                        await session.execute(delete(Role).where(Role.id == item_id))
                        await session.commit()
                        return {"Message" :"Sucessfully Deleted object"}
                except Exception as e:
                        await session.rollback()
                        raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
                finally:
                        await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")


@apirouter.delete("/role/all")
async def delete_all_roles(request : Request,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in Role.roles_required()])>0:
        
                try:
                
                        await session.execute(delete(Role))
                        await session.commit()
                        return {"Message" :"Sucessfully Deleted Rows"}
                except Exception as e:
                        
                        await session.rollback()
                        raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")

                finally:
                        await session.close()

            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")


######################################################
######################################################
# Adding Roles to users
######################################################
@apirouter.post("/addroles")
async def add_user_roles(request : Request, user_roles : RolesUsersModel,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in RolesUsers.roles_required()])>0:
        
                try:
                    data=dict(user_roles)
                    data=dataclass_to_dic(data)
                    
                    user=await session.execute(select(User).filter_by(id=data["user_id"]))
                    
                    role=await session.execute(select(Role).filter_by(id=data["role_id"]))
                
                    if role and user:
                        user_role=RolesUsers(**data)
                    
                        session.add(user_role)
                        await session.commit()
                        return {"Message":"insert has been sucessful"} 
                except Exception as e:
                    await session.rollback()
                    print(e )
                    raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")
                    
                finally:
                    
                    await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")


@apirouter.delete("/deleteroles/{role_id}/{user_id}")
async def delete_user_roles(request : Request,role_id : int,user_id : int,current_user :UserModelLogin = Depends(get_current_active_user),session : AsyncSession=Depends(get_session)):
            available_roles=[x["name"] for x in current_user["roles"]]
            if len([x for x in available_roles if x in RolesUsers.roles_required()])>0:
                try:
                
                        await session.execute(delete(RolesUsers).where(RolesUsers.user_id == user_id).where(RolesUsers.role_id == role_id))
                        await session.commit()
                        return {"Message" :"Sucessfully Deleted Rows"}
                except Exception as e:
                        
                        await session.rollback()
                        raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")

                finally:
                        await session.close()
            else:
                raise HTTPException(status_code=401, detail="Message: you do not have the required privileges for this resource")

######################################################
# Other complimentary routes
######################################################

# from secrets import token_hex
@apirouter.post("/login")
async def login_user(request : Request, login_data : LoginUserModel ,session :AsyncSession=Depends(get_session)):
                
                logdata=dict(login_data)
                print(logdata)
                try:
                        if logdata['grant_type'] =='authorization_code':
                            
                            user=await session.execute(select(User).filter_by(username=logdata['username']).options(joinedload(User.roles)))
                         
                            user=user.unique().scalars().first()
                           
                            data=dict(UserModelAll.parse_obj(user.asdict()))
                            #handling data for nested pydantic and datacalss objects
                            
                            data=dataclass_to_dic(data)
                            # making UUID json serilazable using the str funciton
                          
                            data=uuid_to_str(data)
                            
                           
                            if  pbkdf2_sha512.verify(logdata['password'],data["password"]):
                               
                                exp=datetime.utcnow()+timedelta(hours=4)
                                exp2=datetime.utcnow()+timedelta(hours=5)
                                key=settings.SECRET_KEY 
                               
                                del data["password"]
                                del data["date_registerd"]
                                print('###9')
                                             
                                token=jwt.encode({"data":data,"exp":exp,},key,algorithm="HS256")
                                # print('###11')
                                reftoken=jwt.encode({'data':data,'exp':exp2},key,algorithm="HS256")
                                # print('###10')                               
                                return {"access_token": token,"refresh_token":reftoken, "token_type": "bearer"}
                            return {"Message":"Invalid Password"}
                        elif logdata['grant_type'] == "refresh_token":
                                exp=datetime.utcnow()+timedelta(hours=4)
                                exp2=datetime.utcnow()+timedelta(hours=5)
                                key=settings.SECRET_KEY
                                data=jwt.decode(logdata['token'],key,algorithms="HS256")
                                data=data["data"]
                                token=jwt.encode({'data':data,'exp':exp},key,algorithm="HS256")
                                reftoken=jwt.encode({'data':data,'exp':exp2},key,algorithm="HS256")
                                return {"access_token": token,"refresh_token":reftoken, "token_type": "bearer"}
                        elif logdata['grant_type'] == "token_decode":
                                key=settings.SECRET_KEY
                                data=jwt.decode(logdata['token'],key,algorithms="HS256")
                                return data["data"]
                        else:
                            raise HTTPException(status_code=400, detail="Incorrect username or password")

                except Exception as e:
                        print(e)
                        await session.rollback()
                        raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")

                finally:
                        await session.close()
                        
@apirouter.post("/token")
async def login_token(request : Request, login_data : OAuth2PasswordRequestForm =Depends(),session :AsyncSession=Depends(get_session)):
                
                try:
                                                
                            user=await session.execute(select(User).filter_by(username=login_data.username).options(joinedload(User.roles)))
                            user=user.unique().scalars().first()
                            data=dict(UserModelAll.parse_obj(user.asdict()))
                            #handling data for nested pydantic and datacalss objects
                            data=dataclass_to_dic(data)
                            # making UUID json serilazable using the str funciton
                            data=uuid_to_str(data)
                            
                            print(data)
                            if  pbkdf2_sha512.verify(login_data.password,data["password"]):
                                
                                exp=datetime.utcnow()+timedelta(hours=4)
                                exp2=datetime.utcnow()+timedelta(hours=5)
                                key=settings.SECRET_KEY 
                                del data["password"]
                                del data["date_registerd"]
                                
                                                
                                token=jwt.encode({'data':data,'exp':exp},key,algorithm="HS256")
                                reftoken=jwt.encode({'data':data,'exp':exp2},key,algorithm="HS256")
                               
                                return {"access_token": token,"refresh_token":reftoken, "token_type": "bearer"}
                            else:
                                raise HTTPException(status_code=400, detail="Incorrect username or password")

                except Exception as e:
                        print(e)
                        await session.rollback()
                        raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended")

                finally:
                        await session.close()
                    
#################################################################

