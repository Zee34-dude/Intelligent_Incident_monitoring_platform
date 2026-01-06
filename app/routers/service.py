from fastapi import APIRouter,Depends
from sqlalchemy.orm  import Session

from app.auth import oaut2
from app.auth.dependencies import require_org_role
from .. import schemas
from ..database import get_db
from ..controller import service_controller



router=APIRouter(
    prefix='/service',
    tags=['Services'],
    dependencies=[Depends(oaut2.get_current_user)]  
)

