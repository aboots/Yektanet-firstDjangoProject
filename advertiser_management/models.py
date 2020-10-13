from django.db import models
from django.db.models import Sum


# Create your models here.

class Advertiser(models.Model):
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    name = models.CharField(max_length=200)

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
        self.save()

    @staticmethod
    def getTotalClicks():
        return Advertiser.objects.aggregate(Sum('clicks'))

    def describeMe(self):
        return "this class is made for advertisers!"

    @staticmethod
    def help():
        return "this class has name,clicks,id,views\n" + "and it has setter/getter methods" + "and it extends BaseAdvertising class"

    def getClicks(self):
        return self.clicks

    def incClicks(self):
        self.clicks += 1
        self.save()

    def incViews(self):
        self.views += 1
        self.save()

    def getViews(self):
        return self.views

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='images', default='default.jpg')
    link = models.CharField(max_length=200)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title
        self.save()

    def getImg(self):
        return self.img

    def setImg(self, img):
        self.img = img
        self.save()

    def getLink(self):
        return self.link

    def setLink(self, link):
        self.link = link
        self.save()

    def setAdvertiser(self, advertiser):
        self.advertiser = advertiser
        self.save()

    def describeMe(self):
        return "This is class for Ad object"

    def getClicks(self):
        return self.clicks

    def incClicks(self):
        self.advertiser.incClicks()
        self.clicks += 1
        self.save()
        self.advertiser.save()

    def incViews(self):
        self.advertiser.incViews()
        self.views += 1
        self.save()
        self.advertiser.save()

    def getViews(self):
        return self.views

    def __str__(self):
        return self.title + " by " + self.advertiser.getName()
