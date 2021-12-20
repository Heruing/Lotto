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
