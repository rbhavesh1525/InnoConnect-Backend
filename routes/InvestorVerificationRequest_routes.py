from fastapi import APIRouter

from models.InvestorVerificationRequest_Schema import (
    InvestorVerificationRequest
)

from services.InvestorVerificationRequest_service import (
    submit_verification_request
)

from services.InvestorVerificationRequest_service import (
    get_all_verification_requests
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

@router.get("/all")
def fetch_all_verification_requests():

    return get_all_verification_requests()



@router.put("/approve/{request_id}")
def approve_request(
    request_id: int
):
    return approve_investor_request(
        request_id
    )


@router.put("/reject/{request_id}")
def reject_request(
    request_id: int
):
    return reject_investor_request(
        request_id
    )