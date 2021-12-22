from django.shortcuts import redirect, render
from  datetime import datetime
from .models import Numbers
import requests


numCounts = {}
def refresh(request):
    for i in range(1, 46):
        numCounts[i] = 0
    # 회차 계산
    now  = datetime.now()
    date_to_compare = datetime.strptime("20021207", "%Y%m%d")
    date_diff = now - date_to_compare
    num = int(date_diff.days/7)+1
    
    # 데이터 계산
    number_set = Numbers.objects.all()
    cnt = number_set.count()
    while cnt < num:
        cnt += 1
        url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo='+ str(cnt)
        response = requests.get(url).json()
        # 회차 초과시 중단
        if response['returnValue'] == 'fail': break
        Numbers.objects.create(**response)
    for n in range(1, 46):
        numCounts[n] += Numbers.objects.filter(drwtNo1=n).count()
        numCounts[n] += Numbers.objects.filter(drwtNo2=n).count()
        numCounts[n] += Numbers.objects.filter(drwtNo3=n).count()
        numCounts[n] += Numbers.objects.filter(drwtNo4=n).count()
        numCounts[n] += Numbers.objects.filter(drwtNo5=n).count()
        numCounts[n] += Numbers.objects.filter(drwtNo6=n).count()


def index(request, page=1):
    refresh(request)
    allThing = Numbers.objects.all()
    numbers = allThing.order_by('-pk')[(page-1)*5:page*5]
    pages = list(range(1, (allThing.count()+1)//5))
    sortedNumbers = tuple(map(lambda x: x[0],sorted(numCounts.items(), key= lambda item: item[1])))
    context= {
        'numbers':numbers,
        'pages': pages,
        'bestNumbers': sortedNumbers[:6],
        'worstNumbers': sortedNumbers[-6:],
    }
    return render(request, 'recommend/index.html', context)

def detail(request, num):
    numCount = numCounts[num]
    allThing = Numbers.objects.all()
    allCount = allThing.count()
    winRate = round(numCount / allCount, 5) * 100
    context = {
        'num':num,
        'numCount': numCount,
        'allCount': allCount,
        'winRate': winRate
    }
    return render(request, 'recommend/detail.html', context)