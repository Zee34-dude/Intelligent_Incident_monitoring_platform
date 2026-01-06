from datetime import datetime, timezone
from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from .. import schemas,database,models
from sqlalchemy.orm import Session
from ..hasing import Hash
from ..auth.token import create_access_token
from ..database import get_db

router=APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(
     or_(
        models.User.email == request.username,
        models.User.username == request.username
    )
    ).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Invalid credentials')
    
    if not Hash.verify(user.hashed_password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    if not user.is_verified:
     raise HTTPException(
         status_code=status.HTTP_403_FORBIDDEN,
         detail="Please verify your email before logging in"
        )
    #generate a jwt token and return 
    access_token=create_access_token( data={"sub":user.email})
    return {"access_token":access_token,"token_type":"bearer"}

@router.post('/verify-email')
def verify_email(request:schemas.VerifyEmail,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==request.email).first()
    
    if not user:
          raise HTTPException(status_code=404, detail="User not found")
      
    
    
    verification = (
        db.query(models.EmailVerification)
        .filter(
            models.EmailVerification.user_id == user.id,
            models.EmailVerification.code == request.code,
            models.EmailVerification.is_used == False,
            models.EmailVerification.expires_at > datetime.now(timezone.utc)
        )
        .first()
    )
    if not verification:
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    
    verification.is_used=True
    
    if user.is_verified:
        return {"message": "Already verified"}  
    
    
    user.is_verified = True
    user.verification_code = None
    user.verification_expires_at = None

    db.commit()
    return {"message": "Email verified successfully"}
