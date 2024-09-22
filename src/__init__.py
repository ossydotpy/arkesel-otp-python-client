from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to PyArkesel"}

from src.api.api import otp_router
app.include_router(otp_router)
