from django.urls import path

from . import views

urlpatterns = [
    path('', views.showHomePage, name='homePage'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('createAd/', views.createAd, name='createAd'),
]