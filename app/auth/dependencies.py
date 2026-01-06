from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.oaut2 import get_current_user


def require_org_role(allowed_roles: list[str]):
    def role_checker(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
      

        # Must have required role
        if user.role.upper() not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return user

    return role_checker
