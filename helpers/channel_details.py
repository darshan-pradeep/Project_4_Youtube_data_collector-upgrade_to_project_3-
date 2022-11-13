from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd


def channel_details_gather(link):  
        channel_id_name_logo=[]
        soup=BeautifulSoup(requests.get(link,cookies={'CONSENT':'YES+1'}).text,"html.parser")
        data=re.search(r"var ytInitialData = ({.*});",str(soup.prettify())).group(1)
        json_data=json.loads(data)
        channel_id=json_data['header']['c4TabbedHeaderRenderer']['channelId']
        channel_name=json_data['header']['c4TabbedHeaderRenderer']['title']
        channel_logo=json_data['header']['c4TabbedHeaderRenderer']['avatar']['thumbnails'][2]['url']
        channel_id_name_logo.append({'channel_id':channel_id,'channel_name':channel_name,'channel_logo':channel_logo})
        # print(channel_id_name_logo)
        return channel_id_name_logo





