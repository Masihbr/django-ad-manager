from django.db import models
from django.utils import timezone
from django.urls import reverse


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
    url = models.URLField(default='')
    approve = models.BooleanField(default=False)

    def __str__(self):
        return ("ad_%d" % self.pk)

    def inc_views(self):
        self.views += 1
        self.advertiser.inc_clicks()
        self.save()

    def inc_clicks(self):
        self.clicks += 1
        self.advertiser.inc_views()
        self.save()

    def get_absolute_url(self):
        return reverse('ads')


class BaseData(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    ip = models.GenericIPAddressField()

    class Meta:
        abstract = True


class Click(BaseData):
    def __str__(self):
        return ("click_%d:ad_%d" % (self.pk, self.ad.pk))


class View(BaseData):
    def __str__(self):
        return ("view_%d:ad_%d" % (self.pk, self.ad.pk))
