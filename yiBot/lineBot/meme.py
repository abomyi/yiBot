import random

from bs4 import BeautifulSoup
import requests


def findMeme(keyword):
    googleURL = 'https://www.google.com.tw/search?q={0}&safe=on&source=lnms&tbm=isch'.format(keyword)
    
    result = requests.get(googleURL)
    
    result = BeautifulSoup(result.text, 'html.parser')
    imgs = result.select('body img', limit=5)    #限制5筆，但是返回8筆？？？
    
    imgResult = [img['src'] for img in imgs]
    
    return random.choice(imgResult)
