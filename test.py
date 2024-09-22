from fastapi.testclient import TestClient
from src import app

client = TestClient(app)

def test_generate_otp():
    request_data = {"phone_number": "1234567890"}
    
    response = client.post("/generate-otp", json=request_data)
    
    assert response.status_code == 200

    response_data = response.json()

    assert "code" in response_data
    assert "id" in response_data

    assert response_data["code"] is not None
    assert response_data["id"] is not None



def test_validate_otp():
    generate_response = client.post("/generate-otp", json={"phone_number": "1234567890"})
    
    assert generate_response.status_code == 200
    generate_data = generate_response.json()
    
    otp_id = generate_data["id"]
    otp_code = generate_data["code"]
    
    validate_response = client.post("/validate-otp", json={"id": otp_id, "code": otp_code})
    
    assert validate_response.status_code == 200
    
    validate_data = validate_response.json()
    assert validate_data["message"] == "success"


def test_validate_otp_invalid_code():
    generate_response = client.post("/generate-otp", json={"phone_number": "1234567890"})
    
    assert generate_response.status_code == 200
    generate_data = generate_response.json()
    
    otp_id = generate_data["id"]
    
    invalid_code = "999999"
    validate_response = client.post("/validate-otp", json={"id": otp_id, "code": invalid_code})
    
    assert validate_response.status_code == 401
    
    validate_data = validate_response.json()
    assert "detail" in validate_data

def test_get_otp_status():
    generate_response = client.post("/generate-otp", json={"phone_number": "1234567890"})

    assert generate_response.status_code == 200
    generate_data = generate_response.json()

    otp_id = generate_data["id"]
    code = generate_data["code"]

    otp_status = client.post("get-otp-status", json={"id": otp_id})

    assert otp_status.status_code == 200
    otp_status = otp_status.json()

    assert "status" in otp_status