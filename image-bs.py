from bs4 import BeautifulSoup
from requests import get

keyword = 'cpu'
url = f'https://unsplash.com'

response = get(url+f'/ja/s/%E5%86%99%E7%9C%9F/{keyword}?license=free')
soup = BeautifulSoup(response.text, 'html.parser')
figure = soup.find_all('figure')
img_detail_urls = []
for f in figure:
    a_tag = f.find('a', class_='rEAWd').get('href')
    img_detail_urls.append(url+str(a_tag))

# for img_url in img_detail_urls:
#     response = get(img_url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     a_tags = soup.find_all('a')
#     for a in a_tags:
#         print(a.get('href'))
#     a_tag = a_tags[1]
#     # print(a_tag.get('href'))

img_url = img_detail_urls[0]
response = get(img_url)
soup = BeautifulSoup(response.text, 'html.parser')
a_tags = soup.find_all('a')
for a in a_tags:
    print(a.get('href'))