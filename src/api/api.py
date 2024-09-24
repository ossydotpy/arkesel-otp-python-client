import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from src.otp import OTPCache, ExpiredOTP, InvalidOTPCodeError
from src.otp_service import OTPService

otp_router = APIRouter()

# Initialize the OTP service with cache
otp_cache = OTPCache()
otp_service = OTPService(otp_cache)

class OTPRequest(BaseModel):
    """Request schema for generating a new OTP."""
    phone_number: str = Field(
        ...,
        description="Phone number for which the OTP is being generated. Must be a valid Ghanaian number 233 followed by 9 digits",
        example="233200000000"
    )
    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        """Validate phone number."""
        pattern = re.compile(r'^233\d{9}$')
        if not pattern.match(v):
            raise ValueError("Phone number must start with 233 and be 12 numeric characters long")
        return v

class OTPValidationRequest(BaseModel):
    """Request schema for validating the OTP."""
    id: str = Field(
        ...,
        description="Unique OTP ID assigned during generation.",
        example="25d27781-a482-4d46-96e2-4e27c69f595b"
    )
    code: str = Field(
        ...,
        description="The OTP code sent to the phone number.",
        example="1A2B3C"
    )

class OTPValidationResponse(BaseModel):
    """Response schema for OTP validation status."""
    status: str = Field(
        ...,
        description="Validation status: 'valid', 'invalid', or 'expired'.",
        example="valid"
    )

class OTPStatusRequest(BaseModel):
    """Request schema for checking the OTP status."""
    id: str = Field(
        ...,
        description="Unique OTP ID to check its status.",
        example="abc123"
    )

class OTPStatusResponse(BaseModel):
    """Response schema for OTP status."""
    status: str = Field(
        ...,
        description="OTP status: 'valid' or 'expired'.",
        example="valid"
    )

class OTPResponse(BaseModel):
    """Response schema for generated OTP details."""
    id: str = Field(
        ...,
        description="Unique identifier for the generated OTP.",
        example="abc123"
    )
    generated_at: str = Field(
        ...,
        description="Timestamp when the OTP was generated.",
        example="2024-09-24T12:34:56"
    )
    expiry: str = Field(
        ...,
        description="Timestamp when the OTP will expire.",
        example="2024-09-24T12:39:56"
    )
    ttl: int = Field(
        ...,
        description="Time-to-live (TTL) of the OTP in minutes.",
        example=5
    )
    phone: str = Field(
        ...,
        description="Phone number for which the OTP was generated.",
        example="233200000000"
    )

@otp_router.post("/generate-otp", response_model=OTPResponse, summary="Generate a new OTP", description="Generates a new OTP and sends it to the specified phone number. The OTP will expire after a defined time-to-live (TTL).")
async def generate_otp(request: OTPRequest):
    try:
        # Use the service to generate and send the OTP
        otp = otp_service.generate_otp(phone_number=request.phone_number)
        otp_service.send_otp(otp)
        
        return OTPResponse(
            id=otp.id,
            generated_at=otp.generated_at.isoformat(),
            expiry=otp.expiry_datetime.isoformat(),
            ttl=otp.ttl,
            phone=otp.phone_number
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate OTP")

@otp_router.post("/validate-otp", response_model=OTPValidationResponse, summary="Validate an OTP", description="Validates the OTP code based on the OTP ID. Returns whether the OTP is valid, invalid, or expired.")
async def validate_otp(request: OTPValidationRequest):
    try:
        # Validate the OTP using the service
        otp_service.validate_otp(request.id, request.code)
        return OTPValidationResponse(status="valid")
    except ExpiredOTP:
        return OTPValidationResponse(status="expired")
    except InvalidOTPCodeError:
        return OTPValidationResponse(status="invalid")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to validate OTP")

@otp_router.post("/get-otp-status", response_model=OTPStatusResponse, summary="Get OTP status", description="Check whether an OTP is still valid or has expired based on its OTP ID.")
async def get_otp_status(request: OTPStatusRequest):
    try:
        # Check the OTP status using the service
        status = otp_service.get_otp_status(request.id)
        return OTPStatusResponse(status=status)
    except Exception as e:
        raise HTTPException(status_code=404, detail="OTP not found")
