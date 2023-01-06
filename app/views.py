from django.shortcuts import render
from django.shortcuts import redirect
from .models import Application
from .models import ServiceArea
from .models import Region
import qrcode
import qrcode.image.svg
from io import BytesIO


# Create your views here.
def index(request):
    return render(request, "index.html", context={
        "apps": Application.objects.exclude(shown=False).all().order_by("display_priority"),
        "service_areas": ServiceArea.objects.all(),
        "regions": Region.objects.all()
    })


def detail(request, post_id):
    app = Application.objects.get(pk=post_id)
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(app.url, image_factory=factory, box_size=10)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()

    context = {
        "app": app,
        "svg": svg
    }
    return render(request, "detail.html", context=context)


def login(request):
    response = redirect('accounts/google/login/')
    return response


def about(request):
    return render(request, "about.html", context={})
