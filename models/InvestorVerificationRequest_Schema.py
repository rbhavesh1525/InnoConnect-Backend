from pydantic import BaseModel
from typing import List


class InvestorVerificationRequest(BaseModel):
    full_name: str
    organization_name: str
    designation: str

    investor_type: str

    linkedin_url: str
    organization_website: str

    preferred_industries: List[str]
    startup_stages: List[str]

    min_investment: int
    max_investment: int

    open_for_opportunities: bool