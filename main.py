import os
import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Retrieve environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Check if all environment variables are set
if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME]):
    raise RuntimeError("One or more AWS environment variables are missing!")

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

class UploadData(BaseModel):
    file_name: str
    data: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/upload")
def upload_data(data: UploadData):
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=data.file_name, Body=data.data)
        return {"message": "Data uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
