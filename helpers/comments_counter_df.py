import pandas as pd
from collections import Counter


def comment_counter(parent_comments,reply_commments):
    df1=pd.DataFrame(parent_comments)
    df2=pd.DataFrame(reply_commments)

    counter1=Counter()
    counter1.update(df1['video_id'])
    counter2=Counter()
    counter2.update(df2['video_id'])
    final_count=counter1+counter2
    final=list(final_count.items())
    df3=pd.DataFrame(final,index=None, columns=['video_id','count'])
    # print(df3)
    return df3
