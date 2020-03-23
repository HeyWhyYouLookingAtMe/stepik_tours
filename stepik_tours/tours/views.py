from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class MainView(TemplateView):
    template_name = "tours/index.html"


class DepartureView(TemplateView):
    template_name = "tours/departure.html"


class TourView(TemplateView):
    template_name = "tours/tour.html"
