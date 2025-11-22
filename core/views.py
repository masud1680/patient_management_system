from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.



def homePage(request):       
        is_patient = request.user.groups.filter(name="patient").exists()
             

        return render(request, 'index.html', {"is_patient" : is_patient})


def aboutPage(request):

    return render(request, 'about.html')


def servicePage(request):

    return render(request, 'service.html')

def contactPage(request):

    return render(request, 'contact.html')

def pricePage(request):

    return render(request, 'price.html')