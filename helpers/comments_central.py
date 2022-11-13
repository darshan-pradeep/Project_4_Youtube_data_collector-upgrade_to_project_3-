from helpers import comments_extractor


def main(all_video_ids):
    parent_comments=[]
    reply_comments=[]
    for video_id in all_video_ids:
        p,r=comments_extractor.get_details(video_id)
        parent_comments.extend(p)
        reply_comments.extend(r)
    # csv_creator_from_dict.write_csv(parent_comments,['video_id','parent_comment_id','parent_user_name','parent_comment'],'parent_comments.csv')
    # csv_creator_from_dict.write_csv(reply_comments,['video_id','reply_parent_id','reply_id','reply_user_name','reply_text'],'reply_comments.csv')
    
    print('Completed gathering all comments')
    return parent_comments,reply_comments
    
    