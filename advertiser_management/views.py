from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.generic import RedirectView, FormView

from .forms import AdForm, AdDetailForm
from .models import Ad, Advertiser


class AdDetailRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'detail'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        # ad.incClicks()
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
        return HttpResponseRedirect(reverse('advertiser_management:adDetails', args=(ad_id,)))
