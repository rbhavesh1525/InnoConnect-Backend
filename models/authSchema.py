from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class SignupModel(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="User's full name"
    )

    email: EmailStr = Field(
        ...,
        description="User's email address"
    )

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="User phone number"
    )

    role: Literal["innovator", "investor"]

    password: str = Field(
        ...,
        min_length=8,
        description="User password"
    )

    confirmpassword: str = Field(
        ...,
        min_length=8
    )


class LoginModel(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User's email address"
    )

    password: str = Field(
        ...,
        min_length=8,
        description="User password"
    )


class TokenModel(BaseModel):
    token: str = Field(
        ...,
        description="JWT access token"
    )

    user_id: str = Field(
        ...,
        description="User id"
    )