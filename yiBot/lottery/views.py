from django.shortcuts import render
from lottery.models import WinningNumbers
from django.http.response import HttpResponse
from pyquery import PyQuery as pq
import datetime

# Create your views here.
def lottery(request):
    
    winningNumbers = WinningNumbers.objects.all()[:10]
    for winningNumber in winningNumbers:
        winningNumber.normalNums = winningNumber.normalNums.split(',')

    return render(request, 'lottery/lottery.html', {'winningNumbers':winningNumbers})


def getLotteryNumbers(request):
    lotteryURL = 'http://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx'

    res = pq(lotteryURL)
    lotteryTables = res('table#Lotto649Control_history_dlQuery table')

    for table in lotteryTables.items():
        lotteryInfo = table('tr').eq(1).find('td')
        drawNo = lotteryInfo.eq(0).text()
        drawDate = (lotteryInfo.eq(1).text()).split('/')
        year = int(drawDate[0]) + 1911
        month = int(drawDate[1])
        day = int(drawDate[2])
        drawDate = datetime.date(year, month, day)

        if WinningNumbers.objects.filter(drawNo=drawNo, drawDate=drawDate, lotteryType='大樂透').exists():
            return HttpResponse(True)

        winningNumbers = WinningNumbers()
        winningNumbers.drawNo = drawNo
        winningNumbers.drawDate = drawDate
        winningNumbers.lotteryType = '大樂透'

        lenOfNumbers = len(table('tr').eq(4).find('td'))
        numbers = table('tr').eq(4).items('td')
        for i, number in enumerate(numbers):
            if i == 0:    # 第一個值為「大小順序」
                continue
            elif i == lenOfNumbers - 1:    # 最後一個值為「特別號」
                winningNumbers.specialNum = number.text()
            else:
                winningNumbers.normalNums += number.text()
            if i < lenOfNumbers - 2:
                winningNumbers.normalNums += ','

        winningNumbers.save()

    return HttpResponse(True)





