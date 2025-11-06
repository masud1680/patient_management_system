from django.urls import path
from core.views import homePage, aboutPage, servicePage

urlpatterns = [
    
    path('', homePage, name="home-page"),
    path('about/', aboutPage, name="about-page"),
    path('service/', servicePage, name="service-page"),
]
