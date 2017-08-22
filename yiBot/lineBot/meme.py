import json
import random

from bs4 import BeautifulSoup
import requests


def findMeme(keyword):
    googleURL = 'https://www.google.com.tw/search?q={0}&safe=active&source=lnms&tbm=isch'.format(keyword)
    header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    res = requests.get(googleURL, headers=header)
    
    result = BeautifulSoup(res.text, 'html.parser')
    
    images = [json.loads(div.text)["ou"] for div in result.find_all("div",{"class":"rg_meta"})[:5]]
    image = random.choice(images)
    
    if image.find('https:') < 0:
        # Linebot 僅接受 https之圖像網址，故在此強制取代為https (很糟糕的方法，但是實用)
        image = image.replace('http', 'https')
    
    return image
