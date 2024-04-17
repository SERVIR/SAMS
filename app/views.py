from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Application
from .models import ServiceArea
from .models import Region
from .models import Developer, Scientist
import qrcode
import qrcode.image.svg
from io import BytesIO
from .models import Application


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


def scientist(request, post_id):
    scientist = Scientist.objects.get(pk=post_id)

    context = {
        "staff": scientist,
    }
    return render(request, "developer.html", context=context)


def developer(request, post_id):
    developer = Developer.objects.get(pk=post_id)

    context = {
        "staff": developer,
    }
    return render(request, "developer.html", context=context)


def login(request):
    response = redirect('accounts/google/login/')
    return response


def about(request):
    return render(request, "about.html", context={})


def is_scoscience(user):
    return user.groups.filter(name='scoscience').exists()


@login_required
@user_passes_test(is_scoscience)
def app_table(request):
    applications = Application.objects.all()
    return render(request, 'application_table.html', {'applications': applications})
