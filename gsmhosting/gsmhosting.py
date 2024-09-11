# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from datetime import datetime

# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Thiết lập chế độ headless cho Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Kích hoạt chế độ headless
# chrome_options.add_argument("--disable-gpu")  # Vô hiệu hóa GPU (giúp chạy ổn định hơn trên Windows)
# chrome_options.add_argument("--no-sandbox")  # Tùy chọn an toàn, đặc biệt khi chạy trong container

# Khởi tạo trình duyệt Chrome với các tùy chọn
driver = webdriver.Chrome(options=chrome_options)

# %%
driver.get("https://forum.gsmhosting.com/vbb/f209/")

links = []
raw_links = driver.find_elements(By.CLASS_NAME, "alt1Active")
for link in raw_links:
    a_tag = link.find_element(By.TAG_NAME, "a")
    title = link.text
    href = a_tag.get_attribute("href")

    links.append({'title': title, 'link':href})
for i, link in enumerate(links):
    print(f"{i + 1}: {link['title']} \n{link['link']} \n")

# %%
DAY = 1
MONTH = 7
YEAR = 2024

KEY_WORDS = ["unlock", "hack", "samsung", "s2", "flip", "fold", "knox"]

# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Thiết lập chế độ headless cho Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Kích hoạt chế độ headless
# chrome_options.add_argument("--disable-gpu")  # Vô hiệu hóa GPU (giúp chạy ổn định hơn trên Windows)
# chrome_options.add_argument("--no-sandbox")  # Tùy chọn an toàn, đặc biệt khi chạy trong container

# Khởi tạo trình duyệt Chrome với các tùy chọn
wdriver = webdriver.Chrome(options=chrome_options)

# %%
def get_threads_from_link(wdriver, link):
    thread_links = []
    wdriver.get(link['link'])
    print(link['title'])

    rows = wdriver.find_elements(By.XPATH, "//*[contains(@id, 'thread_title')]")
    times = wdriver.find_elements(By.CSS_SELECTOR, "div.smallfont[style*='text-align:right; white-space:nowrap']")

    for i, (row, time) in enumerate(zip(rows, times)):
        title = row.text
        link = row.get_attribute('href')
        creatAt = time.text 

        pattern = r'(\d{2}-\d{2}-\d{4})'
        match = re.search(pattern, time.text)
        if match:
            creatAt = match.group(1)
        else:
            creatAt = None

        if(creatAt != None): 
            thread_links.append({'title': row.text, 'link':link, 'creatAt': creatAt})
        
        # print(f"Row {i+1}: {title} \n{link} \n{creatAt}\n")

    month_str = str(MONTH).zfill(2)
    day_str = str(DAY).zfill(2)
    year_str = str(YEAR)

    deadline = month_str + '-' + day_str + '-' + year_str

    thread_links_by_deadline = [item for item in thread_links if datetime.strptime(item['creatAt'], '%m-%d-%Y') >= datetime.strptime(deadline, '%m-%d-%Y')]

    thread_links_by_keywords = [item for item in thread_links_by_deadline if any(keyword in item['title'].lower() for keyword in KEY_WORDS)]


    for i, thread_link in enumerate(thread_links_by_keywords):
        print(f"Row {i+1}: {thread_link['title']} \n{thread_link['link']} \n{thread_link['creatAt']}\n")

    return thread_links_by_keywords

# %%
total_thread_links = []
for link in (links):
    total_thread_links += get_threads_from_link(wdriver, link)
wdriver.close()

stt = 1
for thread_link in (total_thread_links):
    print(stt) 
    stt+=1
    print(thread_link['title'])
    print(thread_link['link'])
    print(thread_link['creatAt'])
    print()

# %%
def getDataByLink(webdriver,url):
    webdriver.get(url)
    
    # lay the div co id la edit...
    edit_divs = driver.find_elements(By.CSS_SELECTOR, "table[id^='post']:nth-of-type(-n+5)")
    list_answers = []
    for i, div in enumerate(edit_divs):
        div_id = div.get_attribute("id")    #ex: edit14872555
        id = div_id[4:]                     #ex: 14872555

        #title
        # strong_tags = div.find_elements(By.TAG_NAME, "strong")
        # title = strong_tags[0].text
        # print('Title: ' + title)

        #content
        content = div.find_element(By.ID, f"post_message_{id}").text
        list_answers.append(content)
    return list_answers

# %%
def showAnswers(list_answers, id):
    for i, answer in enumerate(list_answers):
        print(f"Answer {i+1}: {answer}\n")

# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Thiết lập chế độ headless cho Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Kích hoạt chế độ headless
# chrome_options.add_argument("--disable-gpu")  # Vô hiệu hóa GPU (giúp chạy ổn định hơn trên Windows)
# chrome_options.add_argument("--no-sandbox")  # Tùy chọn an toàn, đặc biệt khi chạy trong container

# Khởi tạo trình duyệt Chrome với các tùy chọn
driver = webdriver.Chrome(options=chrome_options)

# %%
list_answers = []
for i, thread_link in enumerate(total_thread_links):
    print(f"Thread {i}: {thread_link['link']}")
    list_answers.append(getDataByLink(driver, thread_link['link']))
driver.quit()

# %% [markdown]
# ### export data .csv

# %%
# export data .csv
MIN_WORDS = 30
import csv
import pandas as pd

# set features
columns = ['Type', 'Link',  'Published', 'Title', 'Content']
data = []

for i, thread_link in enumerate(total_thread_links):
    row = ['youtube', thread_link["link"], thread_link["title"], thread_link["creatAt"], ''.join(list_answers[i][0:5])]
    if len(list_answers[i][0]) >= MIN_WORDS:
        data.append(row)

# %%
import pandas as pd
import os
from datetime import datetime
today = datetime.today().date()

df = pd.DataFrame(data, columns=columns)

file_path = f'../output/output_{today}.xlsx'
if os.path.exists(file_path):
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        df.to_excel(writer, sheet_name=f'gsm_{today}', index=False)
else:
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name=f'gsm_{today}', index=False)

# %%
#print data
for i, thread_link in enumerate(total_thread_links):
    row = [thread_link["link"], thread_link["title"], thread_link["creatAt"]] + list_answers[i][0:5]
    print(i+1)
    if len(list_answers[i][0]) >= MIN_WORDS:
        print(f'Title: {thread_link["title"]}')
        print(f'Link: {thread_link["link"]}')
        print(f'CreatAt:  {thread_link["creatAt"]}')
    
    print (''.join(list_answers[i][0:5]))
    print("======================================================================")

# %%
from transformers import pipeline

# gen model
summarizer = pipeline("summarization")

# sumary text
text = """
Your max_length is set to 50, but your input_length is only 11. Since this is a summarization task, where outputs shorter than the input are typically wanted, you might consider decreasing max_length manually, e.g. summarizer('...', max_length=5)
your long text or conversation goes here . if you have a long text, send a text or a conversation .
"""
summary = summarizer(text, min_length=0, do_sample=False)
print(summary[0]['summary_text'])

# %%
# sumary
# stt = 0
# for ans in list_answers:
#     long_text = "".join(ans[0:5])
#     length = len(long_text)
#     res = []
#     stt += 1
#     print (f'Sumary {stt}: {length} {length//2}')
#     if (length > 10):
#         res = summarizer(long_text, min_length=0, do_sample=False)
#         print(res[0]['summary_text'])
#     else :
#         print (long_text)
print('Success')

# %% [markdown]
# 


