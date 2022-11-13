from pytube import YouTube
import pafy



def details(list_of_video_ids):
    count=0
    remaining=len(list_of_video_ids)
    det=[]
    for video_id in list_of_video_ids:
        try:
            url="https://www.youtube.com/watch?v="+video_id
            # print(url)
            video = YouTube(url)
            video1=pafy.new(url)
            video_views=video.views
            video_author=video.author
            video_duration=video1.duration
            video_likes=video1.likes
            det.append({'video_id':video_id,'video_author':video_author,'video_duration':video_duration,'video_likes':video_likes,'video_views':video_views})
            count+=1
            remaining-=1
        except OSError as e:
            continue
        # print('done: ',count)
        # print('remaining: ',remaining)
    print('Gathered details of all ',len(list_of_video_ids),'videos')
    return det




# def main(list_of_all_video_ids):
#     indiv_vid_details=details(list_of_all_video_ids)
    
#     csv_creator_from_dict.write_csv(indiv_vid_details,['video_id','video_author','video_duration','video_likes','video_views'],'individual_video_details.csv')
    
#     print('Completed ')
    