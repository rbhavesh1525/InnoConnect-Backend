from fastapi import APIRouter, Depends, HTTPException
from models.authSchema import SignupModel,TokenModel,LoginModel

from services.user_services import signup_user
from services.user_services import login_user


router = APIRouter()

@router.post("/signup")
def signup(request : SignupModel):
    try:
        result = signup_user(
            request.name,
            request.email,
            request.password,
            request.confirmpassword,
            request.interests
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user:LoginModel):
    try:
        result = login_user(user.email,user.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

        #