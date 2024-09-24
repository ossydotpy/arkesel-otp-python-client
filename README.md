# arkesel-otp-python-client
Client for Arkesel OTP API.

When using arkesel, annoyingly you have to have two balances:
- one for sms
- one for the otp account

This is a wrapper around the [Arkesel SMS API](https://developers.arkesel.com/#tag/SMS-V2) to use your sms balance to send OTP codes instead of maintaining two balances.

## Installation
1. Clone this repository using Git
2. Navigate into the project directory: `cd arkesel-otp-python-client`
3. Install dependencies using pip: `pip install -r requirements.txt` 
4. Add your arkesel api key to the `.env`. example in [.envexample](/.envexample) file
5. Run the client: `python app.py`

# Use without an api layer
* You can now use this service to handle the entire OTP workflow without needing an API layer
see [example](/otp_as_a_service.py)

## OR with an api layer
### example usage
1. Generate an OTP
```bash
curl -X POST "http://localhost:8000/generate-otp" \
-H "Content-Type: application/json" \
-d '{"phone_number": "233200000000"}'
```

2. Validate the OTP
using the id we generated in step one.
```
curl -X POST "http://localhost:8000/validate-otp" \
-H "Content-Type: application/json" \
-d '{"id": "25d27781-a482-4d46-96e2-4e27c69f595b", "code": "1A2B3C"}'
```

3. Check OTP Status
using the id we generated in step one.
```bash
curl -X POST "http://localhost:8000/get-otp-status" \
-H "Content-Type: application/json" \
-d '{"id": "25d27781-a482-4d46-96e2-4e27c69f595b"}'
```

