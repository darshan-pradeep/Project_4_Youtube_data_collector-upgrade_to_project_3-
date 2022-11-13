import snowflake.connector
import os
import pymongo

   

def top50_snowflakes(cs,list_of_video_ids):
    top_details=[]
    table_name=os.environ['SNOWFLAKES_TABLENAME']
    for video_id in list_of_video_ids:
        query=f"SELECT * from {table_name} where video_id='{video_id}'"
        top_details.extend(cs.execute(query).fetchall())
    # print(top_details)
    return top_details

def mongo(top_details):
    password=os.environ['MONGODB_PASSWORD']
    link="mongodb+srv://mongodb:{a}@cluster0.zg3uh.mongodb.net/?retryWrites=true&w=majority".format(a=password)
    client = pymongo.MongoClient(link)
    all_thumbnails=[]
    db_name=os.environ['MONGODB_DB_NAME']
    coll_name=os.environ['MONGODB_COLL3_NAME']
    database=client[db_name]
    collection=database[coll_name]
    print('Database and Collection for thumbnails accessed successfully')
    for item in top_details:
        obj=collection.find({'video_id':item[0]})
        for i in obj:
            all_thumbnails.append(i['base_64'])
    return all_thumbnails




def main(list_of_video_ids):
    snowflakes_credentials={'account':os.environ['SNOWFLAKES_ACCOUNT'],
                        'user':os.environ['SNOWFLAKES_USER'],
                        'password':os.environ['SNOWFLAKES_PASSWORD'],
                        'database_name':os.environ['SNOWFLAKES_DATABASE'],
                        'schema_name':os.environ['SNOWFLAKES_SCHEMA'],
                        'warehouse_name':os.environ['SNOWFLAKES_WAREHOUSE']}

    ctx = snowflake.connector.connect(
            user=snowflakes_credentials['user'],
            password=snowflakes_credentials['password'],
            account=snowflakes_credentials['account'],
            warehouse=snowflakes_credentials['warehouse_name'],
            database=snowflakes_credentials['database_name'],
            schema=snowflakes_credentials['schema_name']
            )
    cs = ctx.cursor()
    print('Connection established successfully with Snowflakes')
    top_details=top50_snowflakes(cs,list_of_video_ids)
    # print(top_details)
    return top_details
    









    