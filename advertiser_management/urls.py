from django.urls import path

from . import views
from .views import AdDetailRedirectView
from rest_framework.authtoken.views import obtain_auth_token

app_name = "advertiser_management"
urlpatterns = [
    path('', views.HomePageView.as_view(), name='homePage'),
    path('<int:pk>/', AdDetailRedirectView.as_view(), name='detail'),
    path('createAd/', views.AdFromView.as_view(), name='createAd'),
    path('<int:pk>/details/', views.AdDetails.as_view(), name='adDetails'),
    path('searchAd/', views.SearchAdForm.as_view(), name='searchAd'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
