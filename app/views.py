from django.shortcuts import render
from django.shortcuts import redirect
from .models import Application
from .models import ServiceArea
from .models import Region


# Create your views here.
def index(request):
    return render(request, "index.html", context={
        "apps": Application.objects.exclude(shown=False).all().order_by("display_priority"),
        "service_areas": ServiceArea.objects.all(),
        "regions": Region.objects.all()
    })


def detail(request, post_id):
    return render(request, "detail.html", context={"app": Application.objects.get(pk=post_id)})


def login(request):
    response = redirect('accounts/google/login/')
    return response
