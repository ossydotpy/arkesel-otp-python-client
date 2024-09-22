import os
import requests


def send_sms(recipients, sender="YourSenderId", message=None):
    """
    Send an SMS using the Arkesel API.

    Args:
        recipients (list): List of recipient phone numbers.
        sender (str, optional): The sender's name. Defaults to None.
        message (str, optional): The SMS message. Defaults to None.

    Returns:
        str: The response from the server if successful.
    """
    client = requests.Session()

    headers = {
        "api-key": os.getenv("ARKESEL_API_KEY"),
        "Content-Type": "application/json",
    }

    base_url = "https://sms.arkesel.com/api/v2/sms/send"

    sms_payload = {
        "sender": sender,
        "message": message if message else "Thank you for making a purchase.",
        "recipients": recipients,
    }

    try:
        response = client.post(base_url, headers=headers, json=sms_payload)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None
