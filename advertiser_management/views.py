from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, FormView
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny

from .forms import AdForm, AdDetailForm
from .models import Ad, Advertiser, View, Click
from .permissions import IsOwnerOrReadOnly, IsOwner
from .serializers import AdSerializer, AdvertiserSerializer, ViewSerializer, ClickSerializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class AdDetailRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'detail'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        self.url = ad.link
        return ad.link


class HomePageView(generic.ListView):
    template_name = 'advertiser_management/home_page.html'
    context_object_name = 'advertisers_list'

    def get_queryset(self):
        return Advertiser.objects.all()


class AdFromView(FormView):
    form_class = AdForm
    template_name = 'advertiser_management/create_ad.html'

    def form_valid(self, form):
        title1 = form.cleaned_data.get("title")
        advertiser_id1 = form.cleaned_data.get("advertiser_id")
        link1 = form.cleaned_data.get("link")
        img1 = form.cleaned_data.get("img")
        obj1 = Ad.objects.create(
            title=title1,
            img=img1,
            link=link1,
            clicks=0,
            views=0,
            advertiser=Advertiser.objects.get(pk=advertiser_id1)
        )
        obj1.save()
        return HttpResponseRedirect(reverse('advertiser_management:homePage'))


class AdDetails(generic.DetailView):
    model = Ad
    template_name = 'advertiser_management/details_for_each_ad.html'


class SearchAdForm(FormView):
    form_class = AdDetailForm
    template_name = 'advertiser_management/search_page.html'

    def form_valid(self, form):
        ad_id = form.cleaned_data.get('ad_id')
        ad = get_object_or_404(Ad, pk=ad_id)
        return HttpResponseRedirect(reverse('advertiser_management:adDetails', args=(ad_id,)))


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def click_on_ad(self, request, pk=None):
        ad = self.get_object()
        return Response({'link': ad.link})

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAdminUser | IsOwner])
    def get_ad_special_details(self, request, pk=None):
        ad = self.get_object()
        return Response({'id': ad.id,
                         'total clicks': ad.getClicks(),
                         'total views': ad.getViews(),
                         'clicks last 5 hour': ad.getLast5HourClicksCount(),
                         'views last 5 hour': ad.getLast5HourViewsCount(),
                         'clicks per views in general': ad.getClicksPerViews(),
                         'clicks per views in 5 last hours sorted': ad.getClicksPerViewsCompleteList(),
                         'average time between view and click': ad.getAverageBetweenViewAndClick()
                         })


class AdvertiserViewSet(viewsets.ModelViewSet):
    queryset = Advertiser.objects.all()
    serializer_class = AdvertiserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClickViewSet(viewsets.ModelViewSet):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]


class ViewViewSet(viewsets.ModelViewSet):
    queryset = View.objects.all()
    serializer_class = ViewSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]
