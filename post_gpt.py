from create_gpt import create_content, create_headline, create_title
import markdown
import json
import requests
import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

CONTENT = 'スーパーコンピュータ'
CATEGORY = 'パソコン'

category_dict = {'パソコン':[4], 'スマホ/タブレット':[1], 'オーディオ':[6,10], 'キーボード':[8,6] , 'マウス':[9,6]}

def tweet(content):
    ck = os.environ["CONSUMER_KEY"]
    cs = os.environ["CONSUMER_SECRET_KEY"]
    at = os.environ["ACCESS_TOKEN"]
    ats = os.environ["ACCESS_SECRET_TOKEN"]

    try:
        client = tweepy.Client(consumer_key=ck, consumer_secret=cs, access_token=at, access_token_secret=ats)
        res = client.create_tweet(text=content)
        res = res.data
        return res["id"]
    except:
        return "error"



title_list = create_title(theme='パソコン')
for i, title in enumerate(title_list):
    print(f'No.{i+1}の記事を執筆しています')
    headline_list = create_headline(title)
    # 内容をすべて関数内で生成
    md = create_content(title, headline_list)
    html = markdown.markdown(md)
    status = 'draft'
    payload = {'title': title ,'content' : html ,'status' : status, 'categories': category_dict[CATEGORY]}
    headers = {'content-type': "Application/json"}
    # 環境変数 未実行
    r = requests.post("https://mr-insane.net/wp-json/wp/v2/posts", data=json.dumps(payload) , headers=headers, auth=('mr-insane', str(os.environ["REST_API"])) )
    if str(r) != '<Response [201]>':
        print(f'タイトル「{title}」の投稿に失敗しました')
    else:
        print(f'タイトル「{title}」の投稿に成功しました')
        post_url = r.json()['guid']['rendered']
        # ツイート文作成
        # twitter 処理
