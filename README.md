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