from django.shortcuts import redirect, render
from  datetime import datetime
from .models import Numbers
import requests

def refresh(request):
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
    
    return redirect('recommend:index')


def index(request):
    numbers = Numbers.objects.all()
    context= {
        'numbers':numbers
    }
    return render(request, 'recommend/index.html', context)