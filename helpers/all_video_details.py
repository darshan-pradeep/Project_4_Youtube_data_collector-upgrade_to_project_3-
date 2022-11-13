import os

import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

DEVELOPER_KEY = os.environ['YOUTUBE_DEVELOPER_KEY']
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = DEVELOPER_KEY)



def get_vid_details(channelid,number_of_videos):

    # print('Started gathering list of details top 50 videos of all channels')
    video_details=[]
    request = youtube.search().list(
    part="snippet",
    channelId=channelid,
    maxResults=number_of_videos,
    order="date",
    type="video"
    )
    response = request.execute()
    for item in response['items']:
        video_id=item['id']['videoId']
        video_title=item['snippet']['title']
        thumbnail_url=item['snippet']['thumbnails']['high']['url']
        video_details.append({'video_id':video_id,'video_title':video_title,'thumbnail_url':thumbnail_url})
    # print('Finished gathering list of details top 50 videos of all channels')
    return video_details
 
 
