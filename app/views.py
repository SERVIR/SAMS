from django.shortcuts import render
from django.shortcuts import redirect
from .models import Application
from .models import ServiceArea


# Create your views here.
def index(request):
    return render(request, "index.html", context={
        "apps": Application.objects.exclude(shown=False).all(),
        "service_areas": ServiceArea.objects.all()
    })


def detail(request, post_id):
    return render(request, "detail.html", context={"app": Application.objects.get(pk=post_id)})


def login(request):
    response = redirect('accounts/google/login/')
    return response
