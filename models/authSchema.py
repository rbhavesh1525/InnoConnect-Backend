from pydantic import BaseModel, EmailStr, Field
from typing import List

class SignupModel(BaseModel):
    name : str = Field(..., min_length=2, max_length=50, description="User's full name")
    email : EmailStr = Field(..., description="User's email address")
    password : str = Field(..., min_length=6, description="User's password")
    confirmpassword: str = Field(..., min_length=6)
    interests : List[str] = Field(default_factory=list, description="List of user's interests")


class LoginModel(BaseModel):
    email : EmailStr = Field(..., description="User's email address")
    password : str = Field(..., min_length=6, description="User's password")

class TokenModel(BaseModel):
    token : str = Field(..., description="JWT access token")
    user_id : str = Field(..., description="User id")