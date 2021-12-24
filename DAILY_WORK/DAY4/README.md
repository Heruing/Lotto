### 4일차

1. 숫자 정보 화면 만들기
   - 최근 당첨 일자 추가
2. navbar detail number
3. 공 CSS 적용을 위해 view 방식 개선
4. if문으로 ball class 적용

```django
{% if  number < 10 %}
<div class="ball ball0 m-2">{{num}}</div>
{% elif number < 20%}
...
{% endif %}
```

5. 인터뷰

> Q. 로또 추천 사이트가 있다면 무엇을 볼 수 있어야될까요?
>
> 1. (웃음)당연히 번호를 맞춰야지..
> 2. 
>
> Q. 특별한 기능이 있다면 무엇이 좋을까요?
>
> 	1. 생년월일로 번호 뽑기
>  	2. 

<hr>

#### 4일차 배운점

- 장고 html for문 특정 횟수 돌리기

````html
{% with ''|center:숫자 as range %}
{% for _ in range %}
	{{ forloop.counter }}
{% endfor %}
{% endwith %}
````

- 장고 filter OR 연산하기

```python
from django.db.models import Q

filter(Q(condition1) | Q(condition2))
```

- 장고 filter 값 이하/이상

```python
# less than
.filter('값'__lte=0)
# greater than
.filter('값'__gte=0)
```

- 장고 favicon넣기

````python
# settings.py
import os
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
````

````html
<!--base.html-->
{% load static %}
<head>
	...
  <link rel="shortcut icon" type="image/png" href="{% static 'favicon.ico' %}"/>
    ...
````

