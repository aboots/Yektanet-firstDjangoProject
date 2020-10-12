from django.http import HttpResponse
from django.shortcuts import render


def showHomePage(request):
    return HttpResponse("hello")


def detail(request, question_id):
    pass


def createAd(request):
    pass
