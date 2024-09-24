# example flow

from src.otp import OTPCache, InvalidOTPCodeError
from src.otp_service import OTPService

otp_cache = OTPCache()
otp_service = OTPService(cache=otp_cache)

# Step 1: Generate OTP
phone_number = "233200000000"
otp_instance = otp_service.generate_otp(phone_number)
print(otp_instance.code)

# Step 2: Send OTP
otp_service.send_otp(otp_instance)

# Step 3: Validate OTP 
user_input_code = input('otp code:\n> ')
try:
    is_valid = otp_service.validate_otp(otp_instance.id, user_input_code)
    print("OTP is valid." if is_valid else "OTP is invalid.")
except InvalidOTPCodeError as e:
    print(f"Error: {str(e)}")

# Step 4: Check OTP status

status = otp_service.get_otp_status(otp_instance.id)
print(f"-----\nOTP status: {status}")
