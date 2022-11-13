import pymongo
import os



def mongo_read(client,video_id):   
    parent_comments_coll=os.environ['MONGODB_COLL1_NAME']
    reply_comments_coll=os.environ['MONGODB_COLL2_NAME']
    db_name=os.environ['MONGODB_DB_NAME']
    
    db = client.test
    
    database=client[db_name]
    collection1=database[parent_comments_coll]
    collection2=database[reply_comments_coll]
    vidid=video_id
    parent_comment_ids=[]
    parent_comments=collection1.find({'video_id':vidid})
    final=[]
    for parent_comment in parent_comments:
        d={}
        d['parent_user_name']=parent_comment['parent_user_name']
        d['parent_comment']=parent_comment['parent_comment']
        reply=[]
        reply_comments=collection2.find({'reply_parent_id':parent_comment['parent_comment_id']})
        reply_comments_count=collection2.count_documents({'reply_parent_id':parent_comment['parent_comment_id']})
        if reply_comments_count==0:
            reply.append('No replies yet !!')
        else:
            for reply_comment in reply_comments.sort('reply_id',pymongo.ASCENDING): #shows first reply
                #first and latest reply last 
                re={}
                re['reply_user_name']=reply_comment['reply_user_name']
                re['reply_comment']=reply_comment['reply_text']
                reply.append(re)
        d['replies']=reply
        final.append(d)
    return final




def mongo_connector():
    password=os.environ['MONGODB_PASSWORD']
    link="mongodb+srv://mongodb:{a}@cluster0.zg3uh.mongodb.net/?retryWrites=true&w=majority".format(a=password)
    client = pymongo.MongoClient(link)
    return client




def main(video_id):
    client=mongo_connector()
    final_comments=mongo_read(client,video_id)
    return final_comments