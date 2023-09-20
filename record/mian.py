import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import gspread
from google.oauth2.service_account import Credentials

cookies = {
    'wordpress_sec_cc6c935d7c7a1eb6cc40480da3c75861': 'mr-insane%7C1693615872%7CrEHJG199PdnJky2OF2rV7CBr0PM8ZAXeoKzpiQ7lQ8S%7C8cbeeb98adeb135033158a31bad5ddadcdb66a3c00d2a767a3759a4158280e0f',
    'wp-settings-1': 'libraryContent%3Dbrowse%26posts_list_mode%3Dlist',
    'wp-settings-time-1': '1693251553',
    '_ga': 'GA1.1.1225559960.1693442916',
    '__gads': 'ID=b8948bc634833666-2214a70958e300de:T=1693443038:RT=1693443038:S=ALNI_MY-IYj4oIV4KmymuUZKZAHKRTK03A',
    '__gpi': 'UID=00000d8ef6a22507:T=1693443038:RT=1693443038:S=ALNI_MZyz7vDyMlUEzo5fE9rNU5Lqnf-3A',
    'wordpress_test_cookie': 'WP%20Cookie%20check',
    '_ga_K8T5EY9LGD': 'GS1.1.1693442916.1.0.1693442922.0.0.0',
    'wordpress_logged_in_cc6c935d7c7a1eb6cc40480da3c75861': 'mr-insane%7C1693615872%7CrEHJG199PdnJky2OF2rV7CBr0PM8ZAXeoKzpiQ7lQ8S%7Cbddf305f12c42a3fd11781ef882500515f08aaffdf9296c9f0655855b8545ac4',
}

headers = {
    'authority': 'mr-insane.net',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ja-JP,ja;q=0.9,en-JP;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'wordpress_sec_cc6c935d7c7a1eb6cc40480da3c75861=mr-insane%7C1693615872%7CrEHJG199PdnJky2OF2rV7CBr0PM8ZAXeoKzpiQ7lQ8S%7C8cbeeb98adeb135033158a31bad5ddadcdb66a3c00d2a767a3759a4158280e0f; wp-settings-1=libraryContent%3Dbrowse%26posts_list_mode%3Dlist; wp-settings-time-1=1693251553; _ga=GA1.1.1225559960.1693442916; __gads=ID=b8948bc634833666-2214a70958e300de:T=1693443038:RT=1693443038:S=ALNI_MY-IYj4oIV4KmymuUZKZAHKRTK03A; __gpi=UID=00000d8ef6a22507:T=1693443038:RT=1693443038:S=ALNI_MZyz7vDyMlUEzo5fE9rNU5Lqnf-3A; wordpress_test_cookie=WP%20Cookie%20check; _ga_K8T5EY9LGD=GS1.1.1693442916.1.0.1693442922.0.0.0; wordpress_logged_in_cc6c935d7c7a1eb6cc40480da3c75861=mr-insane%7C1693615872%7CrEHJG199PdnJky2OF2rV7CBr0PM8ZAXeoKzpiQ7lQ8S%7Cbddf305f12c42a3fd11781ef882500515f08aaffdf9296c9f0655855b8545ac4',
    'referer': 'https://mr-insane.net/wp-login.php',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

response = requests.get('https://mr-insane.net/wp-admin/edit.php', cookies=cookies, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
elements = soup.find_all('td', class_='views column-views')
article_num = int(str(soup.find('span', class_='displaying-num')).replace('<span class="displaying-num">','').replace('個の項目</span>',''))

sum = 0
for element in elements:
    view = element.text.replace(' ビュー','')
    sum += int(view)

scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file("blog-record-64458ce6beb4.json", scopes=scope)
gc = gspread.authorize(credentials)

SPREADSHEET_KEY = '1CrHrYOA4GbKUeEk0zHlSP9PInqMFPHqfz3UEDlAYFmo'

workbook = gc.open_by_key(SPREADSHEET_KEY)
worksheet = workbook.get_worksheet(0)

col_len = len(worksheet.col_values(5))
today_record_row = col_len + 1

today = datetime.now(timezone('Asia/Tokyo')).strftime('%m月%d日')

# 本日の日付
worksheet.update_cell(today_record_row, 2, today)

# 執筆記事数
yesterday_article_num = int(worksheet.cell(col_len,4).value)
worksheet.update_cell(today_record_row, 3, article_num-yesterday_article_num)

# 合計記事数
worksheet.update_cell(today_record_row, 4, article_num)

# 本日のPV数
today_pv = sum - int(worksheet.cell(9,6).value)
worksheet.update_cell(today_record_row, 5, today_pv)

# 合計PV数
worksheet.update_cell(today_record_row, 6, sum)