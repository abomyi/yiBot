from lineBot.models import Card
import random


def drawCard(msg):
    #===========================================================================
    # 根據機率(權重)隨機抽卡，並且返回N次的抽卡結果
    #===========================================================================
    timesIndex = msg.find('次')
    try:
        times = int(msg[:timesIndex])
    except ValueError:  #格式不符
        times = 1
    except:  #沒指定次數
        times = 1

    cards = Card.objects.all()

    values, weights = [], []
    for card in cards:
        values.append(card.name)
        weights.append(card.weight)

    sum_weights, cumulative_weights = count_sum_weights(weights)

    resultDict = {}
    for i in range(times):
        num_random = random.random() * sum_weights
        index = interval(cumulative_weights, num_random)
        result = values[index]

        if resultDict.get(result):
            resultDict[result] += 1
        else:
            resultDict[result] = 1

    response = ''
    for name, num in resultDict.items():
        response += name + ':' + str(num) + '\n'

    return response


def count_sum_weights(weights):
    sum_weights = 0
    cumulative_weights = []    #累積權重(累積分佈)
    for w in weights:
        sum_weights += w
        cumulative_weights.append(sum_weights)

    return sum_weights, cumulative_weights


def interval(a, x, lo=0, hi=None):
    #===========================================================================
    # 這支func其實就是from bisect import bisect中的bisect_right
    # a = 累積分佈, x = 亂數, lo = 二元搜尋法要用的變數(無關案例), hi = 總共有幾種可能
    # 其判斷邏輯為 看x介於a的哪個區段
    #===========================================================================

    if lo < 0:
        raise ValueError('lo must be non-negative')

    if hi is None:
        hi = len(a)

    while lo < hi:    #二分搜尋法
        mid = (lo + hi) // 2
        if x < a[mid]: hi = mid
        else: lo = mid + 1
    return lo


