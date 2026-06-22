from fastapi import APIRouter

from models.InvestorVerificationRequest_Schema import (
    InvestorVerificationRequest
)

from services.InvestorVerificationRequest_service import (
    submit_verification_request
)

router = APIRouter()

@router.post("/submit/{user_id}")
def submit_verification(
    user_id: str,
    request: InvestorVerificationRequest
):
    return submit_verification_request(
        user_id,
        request
    )