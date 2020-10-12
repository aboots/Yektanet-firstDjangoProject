from django.http import HttpResponse
from django.shortcuts import render
from .models import Ad, Advertiser


def showHomePage(request):
    advertisers_list = Advertiser.objects.all()
    context = {"advertisers_list": advertisers_list}
    ad_lists = Ad.objects.all()
    for ad in ad_lists:
        ad.incViews()
    return render(request, 'advertiser_management/home_page.html', context)

def detail(request, question_id):
    pass


def createAd(request):
    pass
