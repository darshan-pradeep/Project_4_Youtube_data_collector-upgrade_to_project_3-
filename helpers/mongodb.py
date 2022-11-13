import pymongo
from urllib import parse 
import os
import pandas as pd
import base64
import requests

def df_loader_to_mongo(client,db_name,collection_name,comments):
    database=client[db_name]
    collection=database[collection_name]
    collection.insert_many(comments)
    return 1



def get_as_base64(url):
    return base64.b64encode(requests.get(url).content).decode('utf-8')


def create_list_of_dicts(df):
    print(df)
    l=[]
    for i in range(df['thumbnail_url'].shape[0]):
        base_64=get_as_base64(df['thumbnail_url'][i])
        video_id=df[df['thumbnail_url']==df['thumbnail_url'][i]]['video_id'].values
        l.append({'video_id':video_id[0],'base_64':base_64})
        print(video_id[0],' : done')
    return l

def write_thumbnail_as_base64(client,db_name,coll_name,df):
    list_of_dicts_of_base64= create_list_of_dicts(df)
    database=client[db_name]
    collection=database[coll_name]
    collection.insert_many(list_of_dicts_of_base64)
    print('Insertion Successful to mongodb')
    return 1


def mongo_connector(parent_comments,reply_comments,df):
    password=os.environ['MONGODB_PASSWORD']    
    db_name=os.environ['MONGODB_DB_NAME']
     
    link="mongodb+srv://mongodb:{a}@cluster0.zg3uh.mongodb.net/?retryWrites=true&w=majority".format(a=password)
    client = pymongo.MongoClient(link)
    
    coll1_name=os.environ['MONGODB_COLL1_NAME']   
    df_loader_to_mongo(client,db_name,coll1_name,parent_comments)
    print('parent comments inserted successfully')
    
    coll2_name=os.environ['MONGODB_COLL2_NAME']    
    df_loader_to_mongo(client,db_name,coll2_name,reply_comments)
    print('reply comments inserted successfully')
    
    coll3_name=os.environ['MONGODB_COLL3_NAME']
    write_thumbnail_as_base64(client,db_name,coll3_name,df)
    print('base 64 images inserted successfully')


