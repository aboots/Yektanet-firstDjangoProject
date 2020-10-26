from django.urls import path

from . import views
from django.urls import include
from .views import AdDetailRedirectView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'ads', views.AdViewSet)
router.register(r'advertisers', views.AdvertiserViewSet)
router.register(r'clicks', views.ClickViewSet)
router.register(r'views', views.ViewViewSet)


app_name = "advertiser_management"
urlpatterns = [
    path('', include(router.urls)),
    # path('', views.HomePageView.as_view(), name='homePage'),
    # path('<int:pk>/', AdDetailRedirectView.as_view(), name='detail'),
    # path('createAd/', views.AdFromView.as_view(), name='createAd'),
    # path('<int:pk>/details/', views.AdDetails.as_view(), name='adDetails'),
    # path('searchAd/', views.SearchAdForm.as_view(), name='searchAd'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

]
