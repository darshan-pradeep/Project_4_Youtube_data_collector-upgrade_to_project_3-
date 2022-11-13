import pymongo
import os 
import snowflake.connector
import boto3


def mongo():
    password=os.environ['MONGODB_PASSWORD']
    link="mongodb+srv://mongodb:{a}@cluster0.zg3uh.mongodb.net/?retryWrites=true&w=majority".format(a=password)
    client = pymongo.MongoClient(link)
    all_thumbnails=[]
    db_name=os.environ['MONGODB_DB_NAME']
    coll1_name=os.environ['MONGODB_COLL1_NAME']
    coll2_name=os.environ['MONGODB_COLL2_NAME']
    coll3_name=os.environ['MONGODB_COLL3_NAME']
    database=client[db_name]
    
    collection1=database[coll1_name]
    collection1.delete_many({})
    
    collection2=database[coll2_name]
    collection2.delete_many({})
    
    collection3=database[coll3_name]    
    collection3.delete_many({})

    
def snowflakes():
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
    table_name=os.environ['SNOWFLAKES_TABLENAME']
    query=f'TRUNCATE table {table_name}'
    cs.execute(query)

def aws():
    s3=boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']   
    )
    
    bucket_name=os.environ['AWS_BUCKET_NAME']
    
    bucket=s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    return 1
    
 



def main():
    snowflakes()
    mongo()
    aws()
    return 1
