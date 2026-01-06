from datetime import datetime, timedelta, timezone
from fastapi import status,HTTPException

from app.email_verification import send_verification_email
from app.generate_code import generate_verification_code

from ..import models
from .. import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from ..hasing import Hash
code =generate_verification_code()




def get_user(id:int,db:Session):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user

def create_user(request:schemas.User,db:Session): 
    
    try:
        new_user=models.User(
            username=request.username,
            email=request.email,
            hashed_password=Hash.encrypt(request.hashed_password),
            role='user',
            is_verified=False,           
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        
        verification=models.EmailVerification(
            user_id=new_user.id,
            code=code,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
            is_used=False
        )
        db.add(verification)
        db.commit()
        send_verification_email(new_user.email, verification.code)
        return new_user
    except IntegrityError as e:
        db.rollback()
        # Example: email already exists (unique constraint)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unexpected error: {str(e)}"
        )

    except SQLAlchemyError as e:
        db.rollback()
        # General SQL error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
        
    except Exception as e:
        db.rollback()
        # Any other unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )