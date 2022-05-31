# import jwt
from dataclasses import is_dataclass, asdict
from pydantic import BaseModel
from uuid import UUID

# from pydantic.dataclasses import dataclass
###################################################################3
def save_file():
    pass

# def generate_token(data,key,exp):
#     # exp=datetime.datetime.utcnow()+datetime.timedelta(hours=24)
#     # return  jwt.encode(data,key,algorithm="HS256")
#     dat=json.dumps(data)
#     print(dat)
#     return  jwt.encode({'data':dat,'exp':exp},key,algorithm="HS256")

# def token_decode(data,key):
#     return jwt.decode(data,key,algorithms="HS256")



def dataclass_to_dic(pydantic_model):
    
    data=dict(pydantic_model)
    for key, value in data.items():
    # If value satisfies the condition, then store it in new_dict
            if is_dataclass(value):
                data[key] = asdict(value)
                dataclass_to_dic(data[key])
                         
            elif isinstance(value,list):
                
                amended_list=[]
                for x in value:
                    
                    if is_dataclass(value):
                        amended_list.append(dataclass_to_dic(asdict(x))) 
                    elif isinstance(x,BaseModel):
                        amended_list.append(dataclass_to_dic(dict(x)))
                    else:
                        amended_list.append(x)
                data[key]=amended_list               
    return data

def uuid_to_str(pydantic_model):
    data=dict(pydantic_model)
    for key, value in data.items():
        if isinstance(value,UUID):
              data[key] = str(value)  
        
    return data