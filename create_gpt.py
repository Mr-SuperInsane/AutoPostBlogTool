import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ["GPT_API"]

def create_title(theme):
    res = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                'role':'system',
                'content':'指示の通りブログ記事の作成のお手伝いをしてください。'
            },
            {
                'role':'user',
                'content':f'{theme}に関するブログ記事のタイトルを下記の項目に注意して10個考案してください。\n・文字数をそれぞれ20文字前後で書いてください。\n・読点/句読点を除く記号は半角にしてください。\n・箇条書きで出力してください。\n・過去のタイトルと被らないように氣を付けてください。\n・「\"」や「\'」は使用しないでください。'
            }
        ]
    )

    res = res['choices'][0]['message']['content']
    res_list = res.split('\n')
    title_list = []
    for i, r in enumerate(res_list):
        title_list.append(r.replace(f'{i+1}. ',''))

    return title_list

def create_headline(title):
    res = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                'role':'system',
                'content':'指示の通りブログ記事の作成のお手伝いをしてください。'
            },
            {
                'role':'user',
                'content':f'「{title}」というタイトルのブログ記事を書きたいと思います。記事内の見出し(ヘッディング)を下記の項目に注意して考えてください。\n・箇条書きで3~8個出力してください。\n・最後に結論またはまとめのような締めとなる見出しを追加してください。\n・「\"」や「\'」は使用しないでください。'
            }
        ]
    )

    res = res['choices'][0]['message']['content']
    res_list = res.split('\n')
    headline_list = []
    for i, r in enumerate(res_list):
        headline_list.append(r.replace(f'{i+1}. ',''))

    return headline_list
    
def create_content(title, headline):
    res = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                'role':'system',
                'content':'指示の通りブログ記事の作成のお手伝いをしてください。'
            },
            {
                'role':'user',
                'content':f'「{title}」というタイトルのブログ記事の「{headline}」という見出しの内容(記事の本文)を考えてください。内容のみを出力してください。'
            }
        ]
    )

    res = res['choices'][0]['message']['content']
    return res

