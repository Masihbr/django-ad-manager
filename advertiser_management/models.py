from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.


class Advertiser(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='images')
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    url = models.URLField(default='')
    approve = models.BooleanField(default=False)

    def __str__(self):
        return ("ad_%d" % self.pk)

    @staticmethod
    def get_absolute_url():
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
