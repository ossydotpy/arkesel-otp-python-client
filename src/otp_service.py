from src.otp import OTP, InvalidOTPCodeError, OTPCache
from src.utils import send_sms


class OTPService:
    def __init__(self, cache: OTPCache):
        self.cache = cache

    def generate_otp(self, phone_number: str, ttl=5) -> OTP:
        """Generate and store a new OTP."""
        otp = OTP(ttl=ttl, phone_number=phone_number)
        otp.generate()
        self.cache.add(otp)
        return otp

    def send_otp(self, otp: OTP, sender="SenderId"):
        """Send OTP via SMS."""
        message = f"Your OTP code is {otp.code}. Expires at {otp.expiry_datetime}."
        send_sms([otp.phone_number], sender, message)

    def validate_otp(self, otp_id: str, code: str) -> bool:
        """Validate an OTP."""
        otp_instance = self.cache.get(otp_id)
        if not otp_instance:
            raise InvalidOTPCodeError("OTP not found")
        return otp_instance.validate(code)

    def get_otp_status(self, otp_id: str) -> str:
        """Check if OTP is still valid or expired."""
        otp_instance = self.cache.get(otp_id)
        if otp_instance.has_expired():
            return "expired"
        return "valid"
