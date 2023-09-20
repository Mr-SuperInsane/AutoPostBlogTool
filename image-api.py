import requests
import os
import urllib.request
from uuid import uuid4
import cv2
import numpy as np
from PIL import Image

# unsplash apiで画像を取得する

query = 'cpu'

api_key = '8EGNLq5SwIgoW1ObsADuJcF7MpWPxi0Mh0ZaDu4_nEQ'

url = f'https://api.unsplash.com/search/photos?query={query}&page=1&per_page=1'
headers = {'Authorization': f'Client-ID {api_key}'}
response = requests.get(url, headers=headers)
data = response.json()
image_urls = [item['urls']['small'] for item in data['results']]
if not os.path.exists('image'):
    os.makedirs('image')

for i, url in enumerate(image_urls):
    response = urllib.request.urlopen(url)
    data = response.read()
    file_name = str(uuid4())
    file_name += '-' + str(uuid4())
    with open(os.path.join('image', f'temp.jpg'), mode="wb") as f:
        f.write(data)

    # opencvで重点を求める
    img = Image.open('image/temp.jpg')
    parsent = 1920 // img.width
    height = img.height * parsent
    img_resize = img.resize((1920, height), Image.NEAREST)
    img_resize.save(f'image/{file_name}.jpg')


    file_path = f'image/{file_name}.jpg'
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape[:2]

    thresh, img_thresh = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    black_img = np.zeros((h,w),np.uint8)
    cv2.drawContours(black_img, contours, 0, 255, -1)

    M = cv2.moments(black_img, False)
    x,y = int(M["m10"]/M["m00"]) , int(M["m01"]/M["m00"])
    print('mom=('+str(x)+','+str(y)+')')
    cv2.circle(img, (x,y), 10, 255, -1)



# 画像をリサイズする