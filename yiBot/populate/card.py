import os

import django

from lineBot.models import Card


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yibot.settings')
django.setup()


cardList = [('6星 龍拳少年 ‧ 椎拳崇', 16.89), ('6星 烈陽赤炎 ‧ 草薙京', 5.81),
            ('6星 熱血蹴拳王 ‧ 金家藩', 15.64), ('6星 雷光美獸 ‧ 二階堂紅丸', 16.68),
            ('6星 紫藍之月 ‧ 八神庵', 2.97), ('6星 忍術的傳承 ‧ 不知火舞', 6.10),
            ('6星 餓狼狂嚎 ‧ 泰利波格', 17.08), ('6星 超能女高中生 ‧ 麻宮雅典娜', 18.82)]

def populate():
    for name, weight in zip(*cardList):
        Card.objects.create(name=name, weight=weight)

    print('卡片新增完畢')


if __name__ == '__main__':
    populate()