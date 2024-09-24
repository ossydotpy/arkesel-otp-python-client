from datetime import datetime, timezone, timedelta
import secrets
import uuid

class OTP:
    def __init__(self, ttl=5, phone_number: str = None):
        self.code = None
        self.ttl = ttl
        self.generated_at = datetime.now(timezone.utc)
        self.phone_number = phone_number
        self.id = str(uuid.uuid4())

    def generate(self):
        """Generates a 6-character OTP code."""
        self.code = secrets.token_hex(3).upper()

    def validate(self, code: str):
        """
        Validates the given OTP code.
        
        Args:
            code (str): OTP code to validate.
        
        Raises:
            ExpiredOTP: If the OTP has expired.
            InvalidOTPCodeError: If the OTP code is incorrect.
        """
        if self.code == code:
            if self.has_expired():
                raise ExpiredOTP(self.code)
            return True
        else:
            raise InvalidOTPCodeError(self.code)

    def has_expired(self):
        """Check if the OTP has expired based on its TTL."""
        return datetime.now(timezone.utc) > self.expiry_datetime

    @property
    def expiry_datetime(self):
        """Returns the expiration time of the OTP."""
        return self.generated_at + timedelta(minutes=self.ttl)

    def __str__(self):
        return f"OTP Code: {self.code}, Expires At: {self.expiry_datetime}"


class OTPCache:
    def __init__(self):
        """Initialize an in-memory cache for storing OTPs."""
        self.cache = {}

    def add(self, otp_instance: OTP):
        """Add an OTP instance to the cache."""
        self.cache[otp_instance.id] = otp_instance

    def get(self, otp_id: str):
        """Retrieve an OTP from the cache by its ID."""
        return self.cache.get(otp_id)


class OTPErrors(Exception):
    """Base class for OTP-related errors."""
    pass


class ExpiredOTP(OTPErrors):
    """Raised when the OTP has expired."""
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Expired OTP code: {code}")


class InvalidOTPCodeError(OTPErrors):
    """Raised when an invalid OTP code is provided."""
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Invalid OTP code: {code}")
