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

    def incViews(self):
        self.views += 1

    def getViews(self):
        return self.views

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=200)
    imgUrl = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getImgUrl(self):
        return self.imgUrl

    def setImgUrl(self, imgUrl):
        self.imgUrl = imgUrl

    def getLink(self):
        return self.link

    def setLink(self, link):
        self.link = link

    def setAdvertiser(self, advertiser):
        self.advertiser = advertiser

    def describeMe(self):
        return "This is class for Ad object"

    def getClicks(self):
        return self.clicks

    def incClicks(self):
        self.advertiser.incClicks()
        self.clicks += 1

    def incViews(self):
        self.advertiser.incViews()
        self.views += 1

    def getViews(self):
        return self.views

    def __str__(self):
        return self.title + " by " + self.advertiser.getName()
