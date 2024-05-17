from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import date as django_date_format

from .models import Application, Log
from .models import ServiceArea
from .models import Region
from .models import Developer, Scientist
import qrcode
import qrcode.image.svg
from io import BytesIO
from .models import Application



app_version = 1.02

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
        "svg": svg,
        "version": app_version
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


def log_submit(request):
    if request.method == 'POST':
        log_entry_text = request.POST.get('log_entry')
        application_id = request.POST.get('application_id')

        application = get_object_or_404(Application, id=application_id)

        # Create a new log entry
        new_log = Log.objects.create(
            application=application,
            # Replace 'your_application_instance' with the actual application instance
            log_entry=log_entry_text,
            user=request.user  # Assign the current user
        )

        # Return the new log entry as JSON response
        return JsonResponse({'date': django_date_format(new_log.date_modified, "M. j, Y"), 'log_entry': new_log.log_entry})
    else:
        return JsonResponse({'error': 'Invalid request method'})