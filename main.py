from fastapi import FastAPI, Response, Request
from mangum import Mangum
import boto3
import subprocess

app = FastAPI()
handler = Mangum(app)


def save_to_s3(bucket_name, object_key, content):
    # AWS credentials setup (make sure you handle credentials securely)
    aws_access_key = "AKIAZC3RQOWY2DXBO72Q"
    aws_secret_key = "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"

    # Initialize S3 client
    s3 = boto3.client(
        "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
    )

    # Upload content to S3
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=content)


def convert_wav():
    command = [
        "ffmpeg",
        "-i",
        "https://d8cele0fjkppb.cloudfront.net/ivs/v1/624618927537/y16bDr6BzuhG/2023/12/6/10/49/4JCWi1cxMwWo/media/hls/master.m3u8",
        "-b:a",
        "64k",
        "-f",
        "wav",  # Force output format to WAV
        "pipe:1",  # Send output to stdout
    ]

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    bucket_name = 'sagemakerquestions'
    object_key = '657ae0c1ec9a6e346d80318f.WAV'  # Replace with desired object key
    save_to_s3(bucket_name, object_key, stdout)


@app.get("/")
def get_audio():

    convert_wav()
    return {"text": "text"}
