import datetime
import secrets
import uuid

from src.utils import send_sms


class OTP:
    def __init__(self, phone_number, ttl: int = 5):
        """
        Generate an OTP object for a given phone number and expiry time.
        Args:
            phone_number (str): Phone number for which the OTP is being generated.
            ttl (int, optional): Time-to-live in minutes. Defaults to 5.
        """
        self.code = None
        self.generated_at = datetime.datetime.now(datetime.UTC)
        self.expiry_time = ttl * 60
        self.phone_number = phone_number
        self.id = str(uuid.uuid4())

    def generate(self, length=3):
        """Generates a random OTP code of length `length * 2`
        Args:
            length (int): half length of the OTP code to be generated
        Returns: (str): random OTP code
        """
        self.code = secrets.token_hex(length).upper()

    def send_otp(self, sender):
        """
        Sends an OTP to the phone number of this object using SMS.
        Args:
            sender (str): The sender ID for the SMS.
        """
        message = f"Your OTP code is {self.code}. This code will expire in {self.ttl} minutes."
        send_sms([self.phone_number], sender, message)

    def validate(self, code):
        if (
            not self.code
            or (datetime.datetime.now(datetime.UTC) - self.generated_at).total_seconds() > self.expiry_time
        ):
            return False
        elif self.code == code:
            return True
        else:
            raise InvalidOTPCodeError("Invalid OTP code")

    def has_expired(self):
        return (datetime.datetime.now(datetime.UTC) - self.generated_at).total_seconds() >= self.expiry_time

    @property
    def ttl(self):
        return datetime.timedelta(minutes=self.ttl)

    @property
    def expiry_datetime(self):
        return datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=self.ttl)

    def __str__(self):
        return f"OTP Code: {self.code}, Expiration Time: {self.expiry_datetime}"


class OTPCache:
    def __init__(self):
        self.cache = {}

    def add(self, otp_instance):
        self.cache[otp_instance.id] = otp_instance

    def get(self, id):
        return self.cache.get(id)


class OTPErrors(Exception):
    pass


class ExpiredOTPPayload:
    def __init__(self, code: str) -> None:
        self.code = code


class ExpiredOTPError(OTPErrors):
    """Raised when trying to validate an expired OTP."""

    def __init__(self, payload: ExpiredOTPPayload = None) -> None:
        super().__init__()
        self.payload = payload

    @classmethod
    def from_code(cls, code: str):
        return cls(ExpiredOTPPayload(code))


class InvalidOTPCodeError(Exception):
    """Raised when trying to validate an invalid OTP code."""

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message
