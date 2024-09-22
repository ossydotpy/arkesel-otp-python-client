from pydantic import BaseModel

from fastapi import APIRouter, HTTPException
from src.models import OTP, ExpiredOTPError, InvalidOTPCodeError, OTPCache

otp_router = APIRouter()
otp_cache = OTPCache()

class OTPRequest(BaseModel):
    phone_number: str

class OTPValidationRequest(BaseModel):
    id: str
    code: str

class OTPStatusRequest(BaseModel):
    id: str



@otp_router.post("/generate-otp")
async def generate_otp(request: OTPRequest):
    try:
        otp = OTP(ttl=5, phone_number=request.phone_number)
        otp.generate()

        otp_cache.add(otp)

        return {"code": otp.code, "id": otp.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_error_message(e))


@otp_router.post("/validate-otp")
async def validate_otp(request: OTPValidationRequest):
    try:
        otp_instance = otp_cache.get(request.id)

        if not otp_instance:
            raise HTTPException(status_code=400, detail="Invalid ID")

        otp_instance.validate(request.code)

        return {"message": "success"}
    except InvalidOTPCodeError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ExpiredOTPError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@otp_router.post("/get-otp-status")
async def get_otp_status(request: OTPStatusRequest):
    try:
        otp_instance = otp_cache.get(request.id)

        if not otp_instance:
            raise HTTPException(status_code=400, detail="Invalid ID")

        status = "Expired" if otp_instance.has_expired() else "Valid"

        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_error_message(e))


def get_error_message(exception):
    if isinstance(exception, ValueError):
        return "Invalid input"
    elif isinstance(exception, Exception):
        return "Internal server error occurred"
    else:
        return str(exception)