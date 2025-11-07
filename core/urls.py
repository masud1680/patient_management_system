from django.urls import path
from core.views import homePage, aboutPage, servicePage, contactPage,pricePage

urlpatterns = [
    
    path('', homePage, name="home-page"),
    path('about/', aboutPage, name="about-page"),
    path('service/', servicePage, name="service-page"),
    path('contact/', contactPage, name="contact-page"),
    path('price/', pricePage, name="price-page"),
]
