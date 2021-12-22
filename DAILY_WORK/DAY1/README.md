### 1일차

1. 설계하기, README 작성 시작
2. Django 구조 만들어보기(모델 설계)
3. 참고 url : 동행복권 API

```bash
$django-admin startproject Lotto .
$python manage.py createapp recommend
```

````python
#settings.py
INSTALLED_APPS = [
    ...
    'recommend'
    ...
]

TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates',],
        ...
    }
]

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = 'Asia/Seoul'
````



동행복권 json파일을 파로 사용할 수 있도록 모델 설정

````python
from django.db import models

class Numbers(models.Model):
    totSellamnt = models.IntegerField()
    drwNoDate = models.CharField(max_length=10)
    firstWinamnt = models.IntegerField()
    drwNo = models.IntegerField()
    drwtNo1 = models.IntegerField()
    drwtNo2 = models.IntegerField()
    drwtNo3 = models.IntegerField()
    drwtNo4 = models.IntegerField()
    drwtNo5 = models.IntegerField()
    drwtNo6 = models.IntegerField()
    bnusNo = models.IntegerField()
    firstPrzwnerCo = models.IntegerField()
    returnValue = models.CharField(max_length=20)
    firstAccumamnt = models.IntegerField()
````



홈페이지에 활용할 수 있도록 number object 불러오기까지 진행

````html
<!--index.html-->

{% extends 'base.html' %}

{% block content %}
  <h1>로또</h1>
  <a href="{% url 'recommend:refresh' %}"><button>Refresh</button></a>
  {% for number in numbers %}
    {{number}}
  {% endfor %}
{% endblock content %}
````



1일차 view

```python
from django.shortcuts import redirect, render
from datetime import datetime
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
```

1일차 urls.py

```python
from django.urls import path
from . import views

app_name = 'recommend'

urlpatterns = [
    path('/<int:page>', views.index, name='index'),
    path('refresh/', views.refresh, name='refresh'),
]
```



<hr>


#### 1일차 새로 사용 & 배운점

Django json에서 바로 오브젝트 생성하기

```python
{Model Name}.objects.create(**json)
```

날짜 차이 계산하기

```python
from datetime import datetime
now  = datetime.now()
    date_to_compare = datetime.strptime("20021207", "%Y%m%d")
    date_diff = now - date_to_compare
    num = int(date_diff.days/7)+1
```

