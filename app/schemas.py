from pydantic import BaseModel,EmailStr
from typing import Dict, List, Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    viewer = "viewer"
    
class User(BaseModel):
    username:str
    email:EmailStr
    hashed_password:str
    role:UserRole

class ShowUser(BaseModel):
    username:str
    email:EmailStr
    role:UserRole    
    class Config:
        from_attributes = True
    
class VerifyEmail(BaseModel):
    email: EmailStr
    code: str
class OrganizationCreate(BaseModel):
    name:str
    email:str
    user_id:int
    
class Incident(BaseModel):
    note:str
    user_id:int

class ServiceCreate(BaseModel):
    website_name:str
    url:str
    status:str
    
class SeverityDis: 
    LOW: int
    MEDIUM: int
    HIGH: int
    CRITICAL: int
  
      
class ServiceMetrics(BaseModel):
  service_id: int
  uptime_percentage: float
  current_downtime_seconds:int
  total_downtime_seconds: int
  total_uptime_seconds:int
  service_life_time:int
  mttr_seconds: int
  incident_count: int
  severity_distribution: Dict[str, int]
  
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None    