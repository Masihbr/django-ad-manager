from django.db import models

# Create your models here.
class BaseAdvertising(models.Model):
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

class Advertiser(BaseAdvertising):
    name = models.CharField(max_length=150)


class Ad(BaseAdvertising):
    title = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)