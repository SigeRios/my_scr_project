import boto3
from fastapi import FastAPI

app = FastAPI()

s3 = boto3.client('s3')
BUCKET_NAME = 'abdelilahbucket'

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/upload")
def upload_data(file_name: str, data: str):
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=data)
    return {"message": "Data uploaded"}
