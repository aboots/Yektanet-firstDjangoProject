from django.db import models
from django.db.models import Sum

# Create your models here.
from django.utils.datetime_safe import datetime


class Advertiser(models.Model):
    name = models.CharField(max_length=200)

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
        self.save()

    @staticmethod
    def getTotalClicks():
        return Advertiser.objects.aggregate(Sum('clicks')).get('clicks__sum')

    def describeMe(self):
        return "this class is made for advertisers!"

    @staticmethod
    def help():
        return "this class has name,clicks,id,views\n" + "and it has setter/getter methods" + "and it extends BaseAdvertising class"

    def getClicks(self):
        sum1 = 0
        for ad in self.ad_set.all():
            sum1 += ad.getClicks()
        return sum1

    def getViews(self):
        sum1 = 0
        for ad in self.ad_set.all():
            sum1 += ad.getViews()
        return sum1

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='images', default='default.jpg')
    link = models.URLField(max_length=200)
    approve = models.BooleanField(default=False)
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
        return self.click_set.count()

    def incClicks(self, ip):
        obj1 = Click.objects.create(
            ad=self,
            time=datetime.now(),
            user_ip=ip
        )
        obj1.save()

    def incViews(self, ip):
        obj1 = View.objects.create(
            ad=self,
            time=datetime.now(),
            user_ip=ip
        )
        obj1.save()

    def getViews(self):
        return self.view_set.count()

    def isApprove(self):
        return self.approve

    def setApprove(self, approve):
        self.approve = approve

    def __str__(self):
        return self.title + " by " + self.advertiser.getName()


class Click(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)
    user_ip = models.GenericIPAddressField()


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)
    user_ip = models.GenericIPAddressField()
