from django.urls import path

from . import views
from .views import AdDetailRedirectView

urlpatterns = [
    path('', views.showHomePage, name='homePage'),
    path('<int:pk>/', AdDetailRedirectView.as_view(), name='detail'),
    path('createAd/', views.createAd, name='createAd'),
]