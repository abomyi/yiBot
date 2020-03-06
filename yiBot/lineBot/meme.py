import requests
import re
import random
# import json
from bs4 import BeautifulSoup


def findMeme(keyword):
    googleURL = 'https://www.google.com.tw/search?q={0}&safe=active&source=lnms&tbm=isch'.format(keyword)
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
    res = requests.get(googleURL, headers=header)
#     print(res.text)

    result = BeautifulSoup(res.text, 'html.parser')
#     url = re.findall('https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', result.text)

    # 根據返回的文字，直接下正規表達式撈所有影像檔（google將圖檔連結存在倒數第二個script區塊裡面的陣列）
    images = re.findall(r'https://[^"]+\.(?:png|jpe?g|gif)\b', result.find_all('script')[-2].text)

    # 取前五張圖片(熱門搜尋or點擊)
    images = images[:5]
    
#     result = BeautifulSoup(res.text, 'html.parser')
#     print(result.text)
#     images = []
#     for img in result.find_all('img', {'class':'rg_i', 'data-iurl':True}):
#         # result.find_all('div', {'class':'rg_meta'}) # google舊有tag(原圖大小)
# #         image = json.loads(div.text)['ou']
#         if img['data-iurl'].find('https:') != -1:
#             images.append(img['data-iurl'])
#
#         if len(images) >= 5:
#             # 取前五張圖片(熱門搜尋or點擊)即可
#             break
#     images = [json.loads(div.text)['ou'] for div in result.find_all('div',{'class':'rg_meta'})[:5]]  #一行寫法
        
#     if image.find('https:') < 0:
#         # Linebot 僅接受 https之圖像網址，故在此強制取代為https (很糟糕的方法，但是實用)
#         # 後續更新: 不實用，因為部分網站強塞https會產生「此連結網站並不安全...確定要進入此網站?」之狀況，然而Linebot無法處理此情形，故會回傳一個永遠無法載入的圖片給客戶端
#         image = image.replace('http', 'https')

    if not images:
        return None

    img = random.choice(images)
    # 網址可能包含一些unicode字元(例如\u003d)，應該直接用「html.unescape」轉就好，但很詭異的無法轉成功，懷疑是爬到的資料編碼有問題(因為直接打特殊字元是可以轉的，拿img來轉就無效)
    # 所以這裡先將爬到的資料轉成bytes再透過unicode-escape轉回字串，就可以將特殊字元恢復原樣
    return bytes(img, 'utf-8').decode('unicode-escape')
