from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def AboutUs(request):
    return render(request, 'main/about_us.html')
