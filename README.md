# lotto
**간단 설명**

해당 프로젝트는 로또 추천번호 생성 사이트를 만드는 사이트입니다.
프로젝트 생성 복습을 위해 만든 간단한 테스트 사이트입니다.



**설계**

사용할 기술은 Python/Django이며 Javascript와 Bootstrap을 활용하여 추가 UI 구성합니다.
회원 기능은 필요없으며, 로또 1회차부터 최신까지 번호를 데이터 베이스에 저장하여 사용할 예정입니다.
이를 바탕으로 갖은 정보들을 표시하여 확률적으로 나올 가능성이 가장 높은 수를 찾습니다.

**수익**

구글 애드를 통해 수익을 창출합니다.



**과정**

1. 실행될 때, 데이터의 가장 마지막 회차 번호부터 최신 회차까지 데이터를 추가합니다.
2. 이를 바탕으로 원하는 방식의 추천 시스템을 만들어 제공합니다.

<hr>

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

