from create_gpt import create_content, create_headline, create_title
import markdown
import json
import requests

CONTENT = 'ゲーミングパソコン'
CATEGORY = 'パソコン'

category_dict = {'パソコン':[4], 'スマホ/タブレット':[1], 'オーディオ':[6,10], 'キーボード':[8,6] , 'マウス':[9,6]}


title_list = create_title(theme='パソコン')
for title in title_list:
    md = ''
    headline_list = create_headline(title)
    for headline in headline_list:
        content = create_content(title, headline)
        md += f'## {headline}\n\n{content}\n\n'

    html = markdown.markdown(md)
    status = 'draft'
    payload = {'title': title ,'content' : html ,'status' : status, 'categories': category_dict[CATEGORY]}
    headers = {'content-type': "Application/json"}
    r = requests.post("https://mr-insane.net/wp-json/wp/v2/posts", data=json.dumps(payload) , headers=headers, auth=('mr-insane', 'NPfe dyWH EXGY U5WN lQBZ axUB') )
    if str(r) != '<Response [201]>':
        print(f'タイトル「{title}」の投稿に失敗しました')
    else:
        print(f'タイトル「{title}」の投稿に成功しました')
        post_url = r.json()['guid']['rendered']
        # twitter 処理