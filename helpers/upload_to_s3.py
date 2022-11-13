import boto3
import os
from io import BytesIO
from pytube import YouTube

def main(video_id):
    s3=boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']   
    )
    
    bucket_name=os.environ['AWS_BUCKET_NAME']
    buffer = BytesIO()
    url = 'https://www.youtube.com/watch?v='+video_id
    yt = YouTube(url)
    video = yt.streams.get_lowest_resolution()
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    s3 = boto3.client('s3')
    s3.upload_fileobj(buffer,bucket_name,'video.mp4')
    return 1