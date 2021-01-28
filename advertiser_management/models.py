from django.db import models

# Create your models here.
class BaseAdvertising(models.Model):
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    class Meta:
        abstract = True

class Advertiser(BaseAdvertising):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def inc_views(self):
        self.views += 1
        self.save()

    def inc_clicks(self):
        self.clicks += 1
        self.save()

class Ad(BaseAdvertising):
    title = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    url = models.URLField()
    
    def inc_views(self):
        self.views += 1
        self.advertiser.inc_clicks()
        self.save()

    def inc_clicks(self):
        self.clicks += 1
        self.advertiser.inc_views()
        self.save()