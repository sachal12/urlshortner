from django.db import models

class LongToShort(models.Model):
    longurl=models.URLField(max_length=255)
    shorturl=models.CharField(max_length=50,unique=True)
    date=models.DateField(auto_now_add=True)
    clicks=models.IntegerField(default=0)
    dclicks=models.IntegerField(default=0)
    mclicks=models.IntegerField(default=0)
    country = models.CharField(max_length=250)
    country_count = models.CharField(max_length=250)



    