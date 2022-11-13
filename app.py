from flask import Flask,render_template,request,send_from_directory,send_file,redirect
import os
from pytube import YouTube
from io import BytesIO
from helpers import channel_details
from helpers import all_video_details
from helpers import get_individual_video_details
from helpers import insert_all_video_details_to_snowflakes
from helpers import comments_central
from helpers import comments_counter_df
from helpers import mongodb
from helpers import display
from helpers import empty_databases
from helpers import comments_reader
from helpers import upload_to_s3
app=Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path,'static'),'favicon.ico',mimetype='images/favicon.png')


@app.route('/')
@app.route('/homepage',methods=['GET','POST'])
def homepage():
    if request.method=='GET':
        return render_template ('homepage.html')
    if request.method=='POST':
        return render_template ('homepage.html')

@app.route('/channelpage',methods=['POST'])
def channelpage():
    channel_url=request.form.get('channel_url')
    channel_id_name_logo=channel_details.channel_details_gather(channel_url)
    return render_template ('channelpage.html',channel_id_name_logo=channel_id_name_logo)


@app.route('/top50_videos',methods=['POST'])
def top50_videos():
    channel_id=request.form.get('channel_id')
    channel_name=request.form.get('channel_name')
    channel_logo=request.form.get('channel_logo')
    number_of_videos=request.form.get('number_of_videos')
    channel_id_name_logo=request.form.get('channel_id_name_logo')
    all_videos_id_title_thumbnail=all_video_details.get_vid_details(channel_id,number_of_videos)
    list_of_video_ids=[]
    list_of_video_ids=[video_details['video_id'] for video_details in all_videos_id_title_thumbnail]

   
    
    individual_video_id_author_duration_likes_views=get_individual_video_details.details(list_of_video_ids)

    parent_comments,reply_comments=comments_central.main(list_of_video_ids)
  
    
    df=comments_counter_df.comment_counter(parent_comments,reply_comments)
    df3=insert_all_video_details_to_snowflakes.merging(all_videos_id_title_thumbnail,individual_video_id_author_duration_likes_views,channel_id_name_logo,df)
    
    mongodb.mongo_connector(parent_comments,reply_comments,df3)
    top_details=display.main(list_of_video_ids)
    all_thumbnails=display.mongo(top_details)
   
    zipped=zip(top_details,all_thumbnails)
    return render_template('display_all_videos.html',details=zipped)
    
    
@app.route('/deletedatabases',methods=['POST'])
def delete_databases():
    empty_databases.main()
    return render_template ('successfull.html')
    

@app.route('/comments',methods=['POST'])
def comments():
    video_id=request.form.get('vid_id')
    print(video_id)
    final_comments=comments_reader.main(video_id)
    return render_template('comments_print.html',comments=final_comments)

@app.route('/download',methods=['POST'])
def download():
    video_id=request.form.get('vid_id')
    buffer = BytesIO()
    url = 'https://www.youtube.com/watch?v='+video_id
    yt = YouTube(url)
    video = yt.streams.get_lowest_resolution()
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment = True, download_name= 'video.mp4')
    

@app.route('/upload',methods=['POST'])
def upload():
    video_id=request.form.get('vid_id')
    upload_to_s3.main(video_id)
    return render_template ('successfull.html')


if __name__=='__main__':
    app.run(debug=True)
