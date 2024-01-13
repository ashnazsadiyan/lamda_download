from fastapi import FastAPI
from mangum import Mangum
import boto3
import subprocess
import requests

app = FastAPI()
handler = Mangum(app)

aws_access_key = "AKIAZC3RQOWY2DXBO72Q"
aws_secret_key = "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"

# Initialize S3 client
s3 = boto3.client("s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)


def save_to_s3(bucket_name, object_key, content):
    # AWS credentials setup (make sure you handle credentials securely)

    # Upload content to S3
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=content)


# def convert_wav():
#     command = [
#         "ffmpeg",
#         "-i",
#         "https://d8cele0fjkppb.cloudfront.net/ivs/v1/624618927537/y16bDr6BzuhG/2023/12/6/10/49/4JCWi1cxMwWo/media/hls/master.m3u8",
#         "-b:a",
#         "64k",
#         "-f",
#         "wav",  # Force output format to WAV
#         "pipe:1",  # Send output to stdout
#     ]
#
#     process = subprocess.Popen(
#         command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
#     )
#     stdout, stderr = process.communicate()
#     bucket_name = 'reckognitionnew'
#     object_key = '657ae0c1ec9a6e346d80318fs.WAV'  # Replace with the desired object key
#     save_to_s3(bucket_name, object_key, stdout)


@app.get("/")
def get_audio():
    try:
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
        bucket_name = 'reckognitionnew'
        object_key = '657ae0c1ec9a6e346d80318fs.WAV'  # Replace with the desired object key
        save_to_s3(bucket_name, object_key, stdout)
        return {"success": "sucess"}

    except Exception as e:
        print(e)
        return {"message": "something went wrong"}


@app.get('/get')
def get_new_text():
    def lambda_handler(event, context):
        # URL of the stream
        stream_url = 'https://d8cele0fjkppb.cloudfront.net/ivs/v1/624618927537/y16bDr6BzuhG/2023/12/6/5/55/EWxpQleowffw/media/hls/master.m3u8'

        try:
            # Fetching the stream data from the URL
            response = requests.get(stream_url)
            stream_data = response.content

            # S3 bucket and object key where you want to upload the stream
            bucket_name = 'reckognitionnew'
            object_key = '657ae0c1ec9a6e346d80318fs.WAV'

            # Uploading the data to S3
            s3.put_object(Body=stream_data, Bucket=bucket_name, Key=object_key)

            return {
                'statusCode': 200,
            }
        except Exception as e:
            print('Error:', str(e))
            return {
                'statusCode': e
            }
