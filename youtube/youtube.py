# %% [markdown]
# ### Get link

# %% [markdown]
# Doc: https://developers.google.com/youtube/v3/docs/search/list?hl=vi

# %%
strs = ['AIza','SyCXm','llW1PCC','yoOq','Ls5j2Db','ZBltp9','EFqWzI']
api_key = ''.join(strs)

# %%
# limit time query
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_previous_date(month, day):
    today = datetime.now()

    # Lấy ngày của tháng trước
    previous_month_date = today - relativedelta(months=month, days=day)

    # Chuyển đổi sang định dạng yêu cầu "YYYY-MM-DDTHH:MM:SSZ"
    formatted_date = previous_month_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    return formatted_date


# %%
from googleapiclient.discovery import build

# Init YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

def search_youtube(query, date, max_results=150):
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        order="date", # sort: date, rating, relevance, viewCount
        publishedAfter=date, #date
        maxResults=max_results
    )
    response = request.execute()
    return response['items']
        

# %%
query = "samsung+kg+mdm+unlock"
previous_date = get_previous_date(month=0, day=30)
print(previous_date)

search_result = search_youtube(query= query, date=previous_date)

# %%
#ignore title
ignore_word = ["T Mobile", "US Cellular", "Sprint USA", "Unlock Service", "Xfinity USA", "Cricket USA", "FRP", "Boost USA", "Verizon USA", "Spectrum", "Lost mode", "Huawei",
                   "Xiaomi", "screen lock", "TFN", "iphone", "icloud"]

# %%
video_ids = [item['id']['videoId'] for item in search_result]

# %% [markdown]
# ### Get data API

# %%
# get video id
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('v', [None])[0]

# Ví dụ
url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
video_id = get_video_id(url)
print(f'Video ID: {video_id}')

# %%
#print json
import json

def prinJson(data):
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_json)

# %%
import requests

def getVideoInfo(video_id):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",  # Các thông tin muốn lấy (ví dụ: tiêu đề, view, mô tả)
        id=video_id
    )
    response = request.execute()
    video_info = response['items'][0]
    return video_info

def getData(link, video_info):
    title = video_info['snippet']['title']
    description = video_info['snippet']['description']
    published_at = video_info['snippet']['publishedAt']
    return ['youtube', link, published_at, title,  description]
# %%
columns = ['Type', 'Link',  'Published', 'Title', 'Content']
data = []
for i, video_id in enumerate(video_ids):
    video_info = getVideoInfo(video_id)
    link = f"https://www.youtube.com/watch?v={video_id}"
    data_row = getData(link, video_info)
    print(data_row[3])
    data.append(data_row)

# %%
import pandas as pd
import os
from datetime import datetime
today = datetime.today().date()

df = pd.DataFrame(data, columns=columns)

file_path = f'../output/output_{today}.xlsx'
if os.path.exists(file_path):
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        df.to_excel(writer, sheet_name=f'youtube_{today}', index=False)
else:
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name=f'youtube_{today}', index=False)

# %%
print('Success')

# %% [markdown]
# query"
# ("Samsung Knox Guard" OR "Samsung MDM" OR "Samsung KG") AND ("unlock" OR "unfasten" OR "unbolt" OR "open" OR "release" OR "unlatch" OR "disengage" OR "free" OR "unseal" OR "uncover" OR "access") AND ("bypass" OR "circumvent" OR "avoid" OR "sidestep" OR "evade" OR "skip" OR "dodge" OR "work around" OR "ignore" OR "overcome" OR "elude") AND ("removal" OR "elimination" OR "deletion" OR "eradication" OR "extraction" OR "withdrawal" OR "dismissal" OR "expulsion" OR "displacement" OR "ouster" OR "exclusion") AND ("tool" OR "software" OR "method" OR "technique" OR "unlocker" OR "key generator" OR "exploit" OR "vulnerability" OR "APK") AND ("ADB" OR "flash firmware") AND ("guide" OR "tutorial" OR "step-by-step" OR "how-to") AND ("legal" OR "issues" OR "compatibility" OR "support") AND ("community forums" OR "troubleshooting") AND ("2024" OR "updated methods") AND ("Galaxy S-series" OR "Note-series" OR "latest security patch") AND (date:2024-08)
# 
# 32 words only for google search:
# ("Samsung Knox Guard" OR "Samsung MDM" OR "Samsung KG") AND ("unlock" OR "bypass" OR "removal") AND ("tool" OR "method" OR "software" OR "guide") AND ("August 2024" OR "latest update")
# 


