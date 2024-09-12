# %% [markdown]
# ### Get link

# %%
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")  # Kích hoạt chế độ headless

driver = webdriver.Chrome(options=chrome_options)

query = "samsung+kg+mdm+unlock"
driver.get(f"https://www.youtube.com/results?search_query={query}")

# %%
# elem = driver.find_elements(By.CLASS_NAME, "inline-metadata-item")

# for e in elem:
#     print(e.text)

# %%
# filter by "This month" option:
driver.find_element(By.ID, "filter-button").click()

time.sleep(2)

filter = driver.find_elements(By.ID, "endpoint")
for i in filter:
   if(i.text == "This month"):
      i.click()

time.sleep(2)


# %%
# scroll page
i = 10
body = driver.find_element(By.TAG_NAME, 'body') 
while(i > 0):
    k = 5
    while(k >= 0):
        body.send_keys(Keys.PAGE_DOWN)  # Scroll down
        k -= 1
    
    time.sleep(1)
    i -= 1

# %%
# elements = []
def ignore_case(element):
    ignore_word = ["T Mobile", "US Cellular", "Sprint USA", "Unlock Service", "Xfinity USA", "Cricket USA", "FRP", "Boost USA", "Verizon USA", "Spectrum", "Lost mode", "Huawei",
                   "Xiaomi", "screen lock", "TFN", "iphone", "ios", "icloud", "ipad"]
    text = element.text.lower()
    for i in ignore_word:
        if i.lower() in text:
            return True
    else:
        return False

# %%
# get elements:
data = {'titles' : [],
        'links' : [],
        'dates' : [],
        'contents' : []}
elements = []
els = driver.find_elements(By.ID, "video-title")

for c, e in enumerate(els):
    if(e.text != "" and ignore_case(e) != True):
        elements.append(e)
        # print(f"{c} : {e.text}")

# %%
# save to arrays
titles = []
links = []
dates = []
ytlinks = []
descriptions = []

# elem = driver.find_elements(By.TAG_NAME, "a")
for i, e in enumerate(elements):
    link = e.get_attribute('href')
    if "shorts" in link: 
        continue
    links.append(link)
    # titles.append(e.text)
    print(f"{i} - {e.text} - {e.get_attribute('href')}")


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
api_key = 'AIzaSyCXmllW1PCCyoOqLs5j2DbZBltp9EFqWzI'

# %%
#print json
import json

def prinJson(data):
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_json)

# %%
import requests

def getVideoInfo(url, video_id):
    # URL để gọi YouTube Data API
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet,contentDetails,statistics'

    # GET
    response = requests.get(url)
    # check success
    if response.status_code == 200:
        data = response.json()
        video_info = data['items'][0]
        return video_info
    else:
        print(f'Error: {response.status_code}')

def getData(video_info):
    title = video_info['snippet']['title']
    description = video_info['snippet']['description']
    published_at = video_info['snippet']['publishedAt']
    return ['gsm', link, published_at, title,  description]

# %%
columns = ['Type', 'Link',  'Published', 'Title', 'Content']
data = []
for i, e in enumerate(links):
    video_id = get_video_id(e)
    video_info = getVideoInfo(link, video_id)
    data_row = getData(video_info)
    # print(data_row)
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

# %%
# import pandas as pd
# from datetime import datetime
# today = datetime.today().date()

# df = pd.DataFrame(data, columns=columns)

# with pd.ExcelWriter(f'output_{today}.xlsx') as writer:
#    df.to_excel(writer, sheet_name=f'youtube_{today}', encoding='utf-8-sig', index=True)

# %% [markdown]
# query"
# ("Samsung Knox Guard" OR "Samsung MDM" OR "Samsung KG") AND ("unlock" OR "unfasten" OR "unbolt" OR "open" OR "release" OR "unlatch" OR "disengage" OR "free" OR "unseal" OR "uncover" OR "access") AND ("bypass" OR "circumvent" OR "avoid" OR "sidestep" OR "evade" OR "skip" OR "dodge" OR "work around" OR "ignore" OR "overcome" OR "elude") AND ("removal" OR "elimination" OR "deletion" OR "eradication" OR "extraction" OR "withdrawal" OR "dismissal" OR "expulsion" OR "displacement" OR "ouster" OR "exclusion") AND ("tool" OR "software" OR "method" OR "technique" OR "unlocker" OR "key generator" OR "exploit" OR "vulnerability" OR "APK") AND ("ADB" OR "flash firmware") AND ("guide" OR "tutorial" OR "step-by-step" OR "how-to") AND ("legal" OR "issues" OR "compatibility" OR "support") AND ("community forums" OR "troubleshooting") AND ("2024" OR "updated methods") AND ("Galaxy S-series" OR "Note-series" OR "latest security patch") AND (date:2024-08)
# 
# 32 words only for google search:
# ("Samsung Knox Guard" OR "Samsung MDM" OR "Samsung KG") AND ("unlock" OR "bypass" OR "removal") AND ("tool" OR "method" OR "software" OR "guide") AND ("August 2024" OR "latest update")
# 


