from django.shortcuts import render

def contacts(request):
    return render(request, 'ultraproject/contacts.html')

def home(request):
    return render(request, 'ultraproject/home.html')