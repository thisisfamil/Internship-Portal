from pydantic import BaseModel


class StatusUpdate(BaseModel):
    status: str  
    
class Admin(BaseModel):
    name: str
    email: str
    password: str
    
class Admin_login(BaseModel):
    name: str
    password: str
    