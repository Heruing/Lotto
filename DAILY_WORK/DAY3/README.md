### 3일차

1. 숫자 정보 화면 만들기
   - 당첨횟수, 당첨확률
   
     ````html
       <div class="container">
         <h1>로또 {{num}}번 상세 정보</h1>
         <p>당첨된 게임 수: {{numCount}}</p>
         <p>당첨 확률: {{winRate}} %</p>
       </div>
     ````
   
     
   
2. base.html - navbar 추가

3. 홈페이지에 최빈값 등 정보 표시

````html
<h4>가장 자주 등장한 번호</h4>
    {% for number in bestNumbers %}
    <a style="text-decoration: none" href="{% url 'recommend:detail' number %}" class="ball">{{number}} </a>
    {% endfor %}
    <br>
    <h4>가장 적게 등장한 번호</h4>
    {% for number in worstNumbers %}
    <a style="text-decoration: none" href="{% url 'recommend:detail' number %}" class="ball">{{number}} </a>
    {% endfor %}
````

