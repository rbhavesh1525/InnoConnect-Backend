from pydantic import BaseModel
from typing import Optional


class UpdateProfileModel(BaseModel):

    name: str

    headline: Optional[str] = None
    bio: Optional[str] = None

    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    website_url: Optional[str] = None

    profile_image: Optional[str] = None
    cover_image: Optional[str] = None