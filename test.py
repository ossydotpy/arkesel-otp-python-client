from fastapi.testclient import TestClient
from src import app
from src.api.api import otp_cache

client = TestClient(app)

def test_generate_otp():
    request_data = {"phone_number": "233200000000"}
    
    response = client.post("/generate-otp", json=request_data)
    
    assert response.status_code == 200

    response_data = response.json()

    assert "id" in response_data
    assert response_data["id"] is not None
    assert response_data["phone"] == "233200000000"
    assert "generated_at" in response_data
    assert "expiry" in response_data
    assert "ttl" in response_data

def test_validate_otp():
    # Generate OTP
    generate_response = client.post("/generate-otp", json={"phone_number": "233200000000"})
    
    assert generate_response.status_code == 200
    generate_data = generate_response.json()
    otp_id = generate_data["id"]

    # Fetch the OTP instance from the cache to get the code
    otp_instance = otp_cache.get(otp_id)
    otp_code = otp_instance.code
    
    # Validate OTP
    validate_response = client.post("/validate-otp", json={"id": otp_id, "code": otp_code})
    
    assert validate_response.status_code == 200
    validate_data = validate_response.json()
    assert validate_data["status"] == "valid"

def test_validate_otp_invalid_code():
    # Generate OTP
    generate_response = client.post("/generate-otp", json={"phone_number": "233200000000"})
    
    assert generate_response.status_code == 200
    generate_data = generate_response.json()
    otp_id = generate_data["id"]
    
    # invalid OTP code
    invalid_code = "999999"
    validate_response = client.post("/validate-otp", json={"id": otp_id, "code": invalid_code})

    
    # assert validate_response.status_code == 401
    validate_data = validate_response.json()
    assert "status" in validate_data
    assert validate_data["status"] == "invalid"


def test_get_otp_status():
    # Generate OTP
    generate_response = client.post("/generate-otp", json={"phone_number": "233200000000"})
    
    assert generate_response.status_code == 200
    generate_data = generate_response.json()
    otp_id = generate_data["id"]
    
    # Get OTP status
    otp_status = client.post("/get-otp-status", json={"id": otp_id})

    assert otp_status.status_code == 200
    otp_status_data = otp_status.json()
    
    assert "status" in otp_status_data
    assert otp_status_data["status"] == "valid"

def test_get_otp_status_invalid():
    # Attempt to get the status of an invalid OTP ID
    invalid_otp_id = "invalid-id-12345"
    otp_status_response = client.post("/get-otp-status", json={"id": invalid_otp_id})

    assert otp_status_response.status_code == 404
    validate_data = otp_status_response.json()
    assert "detail" in validate_data
    assert validate_data["detail"] == "OTP not found"
