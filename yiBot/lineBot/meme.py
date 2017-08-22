import json
import random

from bs4 import BeautifulSoup
import requests


def findMeme(keyword):
    googleURL = 'https://www.google.com.tw/search?q={0}&safe=active&source=lnms&tbm=isch'.format(keyword)
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
    res = requests.get(googleURL, headers=header)
    
    result = BeautifulSoup(res.text, 'html.parser')
    
#     images = [json.loads(div.text)['ou'] for div in result.find_all('div',{'class':'rg_meta'})[:5]]
    images = []
    for div in result.find_all('div', {'class':'rg_meta'})[:10]:
        image = json.loads(div.text)['ou']
        if image.find('https:') != -1:
            images.append(image)
        
        if len(images) >= 5:
            # 取前五張圖片(熱門搜尋or點擊)即可
            break
        
#     if image.find('https:') < 0:
#         # Linebot 僅接受 https之圖像網址，故在此強制取代為https (很糟糕的方法，但是實用)
#         # 後續更新: 不實用，因為部分網站強塞https會產生「此連結網站並不安全...確定要進入此網站?」之狀況，然而Linebot無法處理此情形，故會回傳一個永遠無法載入的圖片給客戶端
#         image = image.replace('http', 'https')
    
    return random.choice(images)
