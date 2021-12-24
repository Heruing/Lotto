from django.shortcuts import redirect, render
from  datetime import datetime
from .models import Numbers
import requests
from django.db.models import Q
from random import sample


numCounts = {}
numDates = {}
def refresh():
    for i in range(1, 46):
        numCounts[i] = 0
        numDates[i] = 0
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
    
    allNumbers = Numbers.objects.all()
    for n in range(1, 46):
        filteredNum = allNumbers.filter(
            Q(drwtNo1=n) | Q(drwtNo2=n) | Q(drwtNo3=n) | Q(drwtNo4=n) | Q(drwtNo5=n) | Q(drwtNo6=n) | Q(bnusNo=n)
            )
        numCounts[n] += filteredNum.count()
        numDates[n] = filteredNum.order_by('-pk')[0].pk
    return cnt

def index(request, page=1):
    now = datetime.today()
    cnt = refresh()
    allThing = Numbers.objects.all()
    allNumbers = allThing.order_by('-pk')[(page-1)*5:page*5]
    numbers = [
        {'drwNo':allNumbers[n].drwNo,
        'drwNoDate':allNumbers[n].drwNoDate,
        'nums': [
            allNumbers[n].drwtNo1,
            allNumbers[n].drwtNo2,
            allNumbers[n].drwtNo3,
            allNumbers[n].drwtNo4,
            allNumbers[n].drwtNo5,
            allNumbers[n].drwtNo6,
            allNumbers[n].bnusNo
            ]
        }
    for n in range(5)
    ]
    pages = list(range(1, (allThing.count()+1)//5))
    
    sortedNumbers = tuple(map(lambda x: x[0],sorted(numCounts.items(), key= lambda item: item[1])))
    sortedNumDates = tuple(map(lambda x: (x[0], x[1], cnt-x[1]),sorted(numDates.items(), key= lambda item: item[1])))
    
    sortedByDates = tuple(map(lambda x: x[0], sortedNumDates))

    tmp = [0]*46
    recommendNums = []
    for n in range(45):
        tmp[sortedByDates[n]] += 1
        if tmp[sortedByDates[n]] == 2:
            recommendNums.append(sortedByDates[n])
        tmp[sortedNumbers[n]] += 1
        if tmp[sortedNumbers[n]] == 2:
            recommendNums.append(sortedNumbers[n])
        


    context= {
        'numbers':numbers,
        'pages': pages,
        'bestNumbers': reversed(sortedNumbers[-6:]),
        'worstNumbers': sortedNumbers[:6],
        'longNums': sortedNumDates[:5],
        'recommendNums' : recommendNums[:10],
        'cnt': cnt,
        'now': now,
    }
    return render(request, 'recommend/index.html', context)

def detail(request, num):
    cnt = refresh()
    numCount = numCounts[num]
    allNumbers = Numbers.objects.all()
    allCount = allNumbers.count()
    winRate = round(numCount / allCount * 100, 2)
    lastWin = numDates[num]
    winDis =  cnt-lastWin
    recentWin5 = allNumbers.order_by('-pk').filter(
            Q(drwNo__gte=cnt-5) & (
                Q(drwtNo1=num) | Q(drwtNo2=num) | Q(drwtNo3=num) | Q(drwtNo4=num) | Q(drwtNo5=num) | Q(drwtNo6=num) | Q(bnusNo=num)
                )
            )
    recentWin10 = allNumbers.order_by('-pk').filter(
            Q(drwNo__gte=cnt-10) & (
                Q(drwtNo1=num) | Q(drwtNo2=num) | Q(drwtNo3=num) | Q(drwtNo4=num) | Q(drwtNo5=num) | Q(drwtNo6=num) | Q(bnusNo=num)
                )
            )

    context = {
        'num':num,
        'numCount': numCount,
        'allCount': allCount,
        'winRate': winRate,
        'lastWin': lastWin,
        'winDis': winDis,
        'recentWin5': recentWin5,
        'recentWin10': recentWin10,
    }
    return render(request, 'recommend/detail.html', context)

def numbers(request):
    refresh()
    sortedNumbers = tuple(map(lambda x: x[0],sorted(numCounts.items(), key= lambda item: item[1])))
    sortedNumDates = tuple(map(lambda x: (x[0]),sorted(numDates.items(), key= lambda item: item[1])))
    tmp = [0]*46
    recommendNums = []

    x = 0
    for n in range(45):
        tmp[sortedNumDates[n]] += 1
        if tmp[sortedNumDates[n]] == 2:
            recommendNums.append(sortedNumDates[n])
            x += 1
        tmp[sortedNumbers[n]] += 1
        if tmp[sortedNumbers[n]] == 2:
            recommendNums.append(sortedNumbers[n])
            x += 1
    
    num10 = recommendNums[:10]
    num20 = recommendNums[:20]
    recommendNums = []
    x = 0
    while x < 5:
        tmp = sample(num10, 6)
        if not tmp in recommendNums:
            recommendNums.append(tmp)
            x += 1
    
    while x < 10:
        tmp = sample(num20, 6)
        if not tmp in recommendNums:
            recommendNums.append(tmp)
            x += 1


    context = {
        'recommendNums': recommendNums
    }
    return render(request, 'recommend/numbers.html', context)

def random(request):
    randomNums = []
    x = 0
    while x < 10:
        tmp = sample(range(1, 46), 6)
        if not tmp in randomNums:
            randomNums.append(tmp)
            x += 1
    context = {
        'randomNums':randomNums
    }
    return render(request, 'recommend/random.html', context)