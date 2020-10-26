import operator
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
from django.utils.datetime_safe import datetime
from rest_framework.authtoken.models import Token


class Advertiser(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def getName(self):
        return self.name

    def getUser(self):
        return self.user

    def setUser(self, user):
        self.user = user
        self.save()

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
            time=timezone.now(),
            user_ip=ip
        )
        obj1.save()

    def incViews(self, ip):
        obj1 = View.objects.create(
            ad=self,
            time=timezone.now(),
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

    def getLast5HourClicksCount(self):
        list1 = []
        for i in range(5):
            time_threshold = timezone.now() - timedelta(hours=(i + 1))
            results = self.click_set.filter(time__gt=time_threshold).count()
            if i > 0:
                sum1 = 0
                for j in range(i):
                    sum1 += list1[j]
                results -= sum1
            list1.append(results)
        return list1

    def getLast5HourViewsCount(self):
        list2 = []
        for i in range(5):
            time_threshold = timezone.now() - timedelta(hours=(i + 1))
            results = self.view_set.filter(time__gt=time_threshold).count()
            if i > 0:
                sum1 = 0
                for j in range(i):
                    sum1 += list2[j]
                results -= sum1
            list2.append(results)
        return list2

    def getClicksPerViews(self):
        if self.view_set.count() != 0:
            x = self.click_set.count() / self.view_set.count()
        else:
            x = 0
        return round(x, 3)

    def getClicksPerViewsCompleteList(self):
        list_clicks = self.getLast5HourClicksCount()
        list_views = self.getLast5HourViewsCount()
        dictionary1 = {}
        for i in range(5):
            if list_views[i] != 0:
                x = list_clicks[i] / list_views[i]
                x = round(x, 3)
            else:
                x = 0
            time_threshold = timezone.now() - timedelta(hours=(i + 1))
            dictionary1['hour ' + str(time_threshold.hour)] = x
        sorted_dictionary1 = sorted(dictionary1.items(), key=operator.itemgetter(1))
        sorted_dictionary1.reverse()
        return sorted_dictionary1

    def getAverageBetweenViewAndClick(self):
        sum1 = 0
        for click1 in self.click_set.all():
            for view1 in self.view_set.all():
                if view1.getIp() == click1.getIp() and view1.getTime() < click1.getTime():
                    selected_view = view1
            time2 = click1.getTime() - selected_view.getTime()
            sum1 += time2.seconds
        avg = round(sum1 / self.click_set.count(), 3)
        print('average seconds : ' + str(avg))
        string_average_time = str(timedelta(seconds=avg))
        return string_average_time


class Click(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)
    user_ip = models.GenericIPAddressField()

    def getIp(self):
        return self.user_ip

    def getTime(self):
        return self.time

    def setIp(self, ip):
        self.user_ip = ip

    def __str__(self):
        return 'click for ad with id ' + self.ad.id.__str__() + ' with ip ' + self.getIp()


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)
    user_ip = models.GenericIPAddressField()

    def getIp(self):
        return self.user_ip

    def getTime(self):
        return self.time

    def setIp(self, ip):
        self.user_ip = ip

    def __str__(self):
        return 'view for ad with id ' + self.ad.id.__str__() + ' with ip ' + self.getIp()
