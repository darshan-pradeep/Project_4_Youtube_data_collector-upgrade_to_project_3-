from urllib import parse 
import pandas as pd
from sqlalchemy import create_engine 
import os
from sqlalchemy.dialects import registry



def merging(all_videos_id_title_thumbnail,individual_video_id_author_duration_likes_views,channel_id_name_logo,df):
    video_details_df=pd.DataFrame(all_videos_id_title_thumbnail)
    # print(df1)
    # df1=df1.to_html()
    individual_details_df=pd.DataFrame(individual_video_id_author_duration_likes_views)
    # print(df2)
    channel_details_df=pd.DataFrame(eval(channel_id_name_logo))
    # print(df3)
    comments_count_df=df
    
    df1=individual_details_df.merge(video_details_df,left_on='video_id',right_on='video_id')
    df2=df1.merge(channel_details_df,left_on='video_author',right_on='channel_name')
    df3=df2.merge(comments_count_df,left_on='video_id',right_on='video_id')
    
    snowflakes_writer(df3)
    return df3



def snowflakes_writer(df):
    snowflakes_credentials={'account':os.environ['SNOWFLAKES_ACCOUNT'],
                        'user':os.environ['SNOWFLAKES_USER'],
                        'password':os.environ['SNOWFLAKES_PASSWORD'],
                        'database_name':os.environ['SNOWFLAKES_DATABASE'],
                        'schema_name':os.environ['SNOWFLAKES_SCHEMA'],
                        'warehouse_name':os.environ['SNOWFLAKES_WAREHOUSE'],
                        'table_name':os.environ['SNOWFLAKES_TABLENAME']}
    account_identifier = snowflakes_credentials['account']
    user = snowflakes_credentials['user']
    password = parse.quote(snowflakes_credentials['password'])
    database_name = snowflakes_credentials['database_name']
    schema_name = snowflakes_credentials['schema_name']
    conn_string = f"snowflake://{user}:{password}@{account_identifier}/{database_name}/{schema_name}"
    registry.register('snowflake', 'snowflake.sqlalchemy', 'dialect')
    engine = create_engine(conn_string) 
    print('Connection established successfully with snowflakes')
    table_name = snowflakes_credentials['table_name']


    if_exists = 'append'   
    warehouse='use warehouse {warehouse_name}'.format(warehouse_name=snowflakes_credentials['warehouse_name'])
    engine.execute(warehouse)
    with engine.connect() as con:
            df.to_sql(name=table_name.lower(), con=con, if_exists=if_exists, index=False) 
    print('Writing to snowflakes completed ')
    engine.dispose()
    