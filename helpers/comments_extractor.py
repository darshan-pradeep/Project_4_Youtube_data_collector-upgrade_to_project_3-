import os
import googleapiclient.discovery
import pandas as pd

DEVELOPER_KEY = os.environ['YOUTUBE_DEVELOPER_KEY']
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = DEVELOPER_KEY)


def car(items,videoId,comments,all_replies):
    try:
        for item in items:

            if 'replies' in item:
                parent_comment_id=item['snippet']['topLevelComment']['id']
                parent_comment=item['snippet']['topLevelComment']['snippet']['textOriginal']
                parent_user_name=item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comments.append({'video_id':videoId,'parent_comment_id':parent_comment_id,'parent_user_name':parent_user_name,
                                'parent_comment':parent_comment})
                for reply in item['replies']['comments']:
                    reply_id=reply['id']
                    reply_text=reply['snippet']['textOriginal']
                    reply_parent_id=reply['snippet']['parentId']
                    reply_user_name=reply['snippet']['authorDisplayName']
                    all_replies.append({'video_id':videoId,'reply_parent_id':reply_parent_id,'reply_id':reply_id,
                                        'reply_user_name':reply_user_name,'reply_text':reply_text})
            else:
                parent_comment_id=item['snippet']['topLevelComment']['id']
                parent_comment=item['snippet']['topLevelComment']['snippet']['textOriginal']
                parent_user_name=item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comments.append({'video_id':videoId,'parent_comment_id':parent_comment_id,'parent_user_name':parent_user_name,
                                'parent_comment':parent_comment})
    except Exception as e:
        print(e)        
    return comments,all_replies



def get_details(videoID):
    comments=[]
    all_replies=[]
    all_parent_comments=[]
    all_reply_comments=[]
    try:
        request = youtube.commentThreads().list(part="id,snippet,replies",videoId=videoID)
        response = request.execute()
        all_parent_comments,all_reply_comments=car(response['items'],videoID,comments,all_replies)

        
        while 'nextPageToken' in response:
            request = youtube.commentThreads().list(part="id,snippet,replies",videoId=videoID,
                                                    pageToken=response['nextPageToken'])
            response = request.execute()
            all_parent_comments,all_reply_comments=car(response['items'],videoID,all_parent_comments,all_replies)
    except Exception as e:
        print(e)
        
    print('Done')
    return all_parent_comments,all_reply_comments
    
