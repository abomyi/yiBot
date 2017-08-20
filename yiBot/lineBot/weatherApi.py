from yiBot.settings import WEATHER_API_KEY
import requests
import json


def weatherApi(text):
    
    apiUrl = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?locationName={0}&Authorization={1}'.format(WEATHER_API_KEY)
    response = requests.get(apiUrl, verify=False)
    jsonDate = json.loads(response.text)
    print(jsonDate['records']['location'][0]['locationName'])
    print(jsonDate['records']['location'][0]["weatherElement"][3])
    
#     'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=WEATER_API_KEY'
    
    return ''


# 來源：http://e-service.cwb.gov.tw/wdps/obs/state.htm
# 一堆地點根本查不到，浪費我時間整理
weatherStation = ['五分山雷達站', '板橋', '淡水', '鞍部', '臺北', '竹子湖', '基隆', '彭佳嶼', '花蓮', '新屋', '蘇澳', '宜蘭', '金門', '東吉島', '澎湖', 
                  '臺南', '永康', '高雄', '嘉義', '臺中', '阿里山', '大武', '玉山', '新竹', '恆春', '成功', '蘭嶼', '日月潭', '臺東', '梧棲', '墾丁雷達站', 
                  '馬祖', '山佳', '坪林', '四堵', '泰平', '福山', '桶後', '屈尺', '石碇', '火燒寮', '瑞芳', '大坪', '五指山', '福隆', '雙溪', '富貴角', '三和', 
                  '金山', '鼻頭角', '三貂角', '社子', '大直', '石牌', '天母', '士林', '內湖', '南港', '三重', '大屯山', '三峽', '信義', '文山', '新莊', '三芝', 
                  '八里', '蘆洲', '土城', '鶯歌', '中和', '汐止', '永和', '五分山', '平等', '林口', '松山', '復興', '桃園', '八德', '中壢', '埔心', '觀音', 
                  '蘆竹', '大溪', '平鎮', '楊梅', '龍潭', '龜山', '梅花', '關西', '峨眉', '打鐵坑', '橫山', '雪霸', '竹東', '香山', '寶山', '新豐', '湖口', 
                  '新竹市東區', '竹南', '南庄', '大湖', '三義', '後龍', '明德', '通霄', '馬都安', '頭份', '造橋', '苗栗', '銅鑼', '卓蘭', '西湖', '獅潭', '苑裡', 
                  '大河', '觀霧2', '高鐵苗栗', '大肚', '雪山圈谷', '石岡', '中坑', '東勢', '梨山', '大甲', '大坑', '中竹林', '神岡', '大安', '后里', '豐原', 
                  '大里', '潭子', '清水', '外埔', '龍井', '烏日', '西屯', '南屯', '新社', '大雅(中科園區)', '桃山', '雪山東峰', '芬園', '鹿港', '員林', '溪湖', 
                  '溪州', '二林', '大城', '竹塘', '高鐵彰化', '福興', '秀水', '花壇', '埔鹽', '埔心', '田尾', '埤頭', '北斗', '田中', '社頭', '芳苑', '二水', 
                  '伸港', '埔里', '中寮', '草屯', '昆陽', '神木村', '合歡山', '廬山', '信義', '鳳凰', '竹山', '水里', '魚池', '集集', '仁愛', '名間', '國姓', 
                  '南投', '梅峰', '萬大林道', '玉山風口', '草嶺', '崙背', '四湖', '宜梧', '虎尾', '土庫', '斗六', '北港', '西螺', '褒忠', '二崙', '大埤', '斗南', 
                  '林內', '莿桐', '古坑', '元長', '水林', '雲林東勢', '臺西', '蔦松', '棋山', '高鐵雲林', '馬頭山', '東後寮', '奮起湖', '中埔', '朴子', '溪口', 
                  '大林', '太保', '水上', '竹崎', '東石', '番路', '嘉義市東區', '六腳', '布袋', '民雄', '嘉義梅山', '鹿草', '新港', '茶山', '里佳', '達邦', 
                  '山美', '曾文', '北寮', '王爺宮', '大內', '善化', '玉井', '安南', '崎頂', '虎頭埤', '新市', '媽廟', '尾寮山', '阿禮', '瑪家', '三地門', 
                  '鹽埔新圍', '屏東', '赤山', '潮州', '來義', '春日', '琉球嶼', '檳榔', '貓鼻頭', '墾丁', '佳樂水', '枋寮', '楓港', '牡丹池山', '東港', '高樹', 
                  '長治', '九如', '竹田', '萬丹', '崁頂', '林邊', '佳冬', '新埤', '新園', '麟洛', '南州', '里港', '舊泰武', '墾雷', '紅葉山', '太麻里', '知本', 
                  '鹿野', '綠島', '池上', '向陽', '紅石', '大溪山', '金崙', '東河', '長濱', '南田', '關山', '大禹嶺', '天祥', '新城', '鯉魚潭', '西林', '光復', 
                  '月眉山', '水源', '富世', '和中', '大坑', '水璉', '鳳林山', '加路蘭山', '豐濱', '靜浦', '雙連埤', '礁溪', '壯圍', '玉蘭', '冬山', '太平山', 
                  '思源', '龜山島', '東澳', '南澳', '五結', '表湖', '復興', '甲仙', '月眉', '美濃', '溪埔', '內門', '古亭坑', '阿公店', '鳳山', '鳳森', '新興', 
                  '旗津', '阿蓮', '梓官', '永安', '茄萣', '湖內', '彌陀', '岡山', '楠梓', '仁武', '鼓山', '三民', '苓雅', '林園', '大寮', '旗山', '路竹', 
                  '橋頭', '大社', '萬山', '六龜', '左營', '東莒', '西嶼', '花嶼', '金沙', '金寧', '烏坵', '東引', '東河', '下營', '佳里', '臺南市北區', 
                  '臺南市南區', '麻豆', '官田', '西港', '安定', '仁德', '關廟', '山上', '安平', '左鎮', '白河', '學甲', '鹽水', '關子嶺', '新營', '後壁', 
                  '柳營', '將軍', '北門', '鹿寮', '七股', '明里', '佳心', '玉里', '舞鶴', '富源', '東華', '吉安光華', '鳳林', '萬榮', '豐裡', '蕃薯寮', 
                  '下盆', '公館', '四十份', '關渡', '水尾', '新埔', '鳥嘴山', '白蘭', '太閣南', '飛鳳山', '外坪(五指山)', '象鼻', '松安', '鳳美', '新開', 
                  '南勢', '南礦', '南勢山', '南湖', '八卦', '馬拉邦山', '泰安', '公館', '上谷關', '稍來', '新伯公', '雪嶺', '桐林', '白冷', '白毛台', '龍安', 
                  '伯公龍', '慶福山', '烏石坑', '清水林', '德基', '下水埔', '翠峰', '瑞岩', '清流', '長豐', '雙冬', '六分寮', '阿眉', '萬大', '武界', '丹大', 
                  '和社', '溪頭', '大鞍', '桶頭', '卡奈托灣', '青雲', '中心崙', '蘆竹湳', '樟湖', '九份二山', '外大坪', '鯉潭', '北坑', '埔中', '豐丘', '西巒', 
                  '奧萬大', '楓樹林', '新興橋', '凌霄', '翠華', '新高口', '望鄉山', '杉林溪', '大尖山', '線浸林道', '口湖', '龍美', '菜瓜坪', '獨立山', '大湖', 
                  '頭凍', '石磐龍', '瑞里', '沙崙', '環湖', '大棟山', '關山', '楠西', '口社', '上德文', '龍泉', '力里', '石門山', '旭海', '車城', '枋山', '牡丹', 
                  '大漢山', '西大武山', '土阪', '都蘭', '下馬', '摩天', '華源', '金峰', '豐南', '利嘉', '南美山', '壽卡', '洛韶', '慈恩', '布洛灣', '東壙', '中興', 
                  '大觀', '太安', '大農', '龍澗', '高寮', '牛鬥', '古魯', '北關', '大礁溪', '再連', '三星', '寒溪', '新寮', '南山', '烏石鼻', '東澳嶺', '觀音海岸', 
                  '頭城', '達卡努瓦', '排雲', '南天池', '梅山', '小關山', '高中', '御油山', '大津', '尖山', '吉東', '溪南(特生中心)', '新發', '藤枝', '多納林道', '東原', 
                  '卓樂', '紅葉', '立山', '壽豐', '銅門']