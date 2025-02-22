from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import date as django_date_format

from .models import Application, Log, Feedback, Like
from .models import ServiceArea
from .models import Region
from .models import Developer, Scientist
import qrcode
import qrcode.image.svg
from io import BytesIO
from .models import Application
from .custom_forms import UserRoleForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

app_version = 1.10


# Create your views here.
def index(request):
    print("hello")
    is_new_user = request.session.get('is_new_user', False)
    if is_new_user:
        del request.session['is_new_user']
        return HttpResponseRedirect('fill_information')
    user = request.user
    is_staff_or_contributor = user.is_staff or user.groups.filter(name="contributors").exists()
    context = {"apps": Application.objects.exclude(shown=False).all().order_by("display_priority"),
               "service_areas": ServiceArea.objects.all(), "regions": Region.objects.all(),
               "is_staff_or_contributor": is_staff_or_contributor, "version": app_version}

    return render(request, "index.html", context=context)


def detail1(request, post_id):
    app = Application.objects.get(pk=post_id)
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(app.url, image_factory=factory, box_size=10)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()
    total_likes_count = app.like_set.count()
    if request.user.is_authenticated:
        i_like = Like.objects.filter(application=app, user=request.user).exists()
    else:
        i_like = False

    if i_like:
        total_likes_count -= 1

    context = {"app": app, "svg": svg, "version": app_version, "i_like": i_like, "total_likes_count": total_likes_count}
    return render(request, "detail1.html", context=context)


def detail(request, post_id):
    app = Application.objects.get(pk=post_id)
    last_updated = get_last_updated(app)
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(app.url, image_factory=factory, box_size=10)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()
    total_likes_count = app.like_set.count()
    if request.user.is_authenticated:
        i_like = Like.objects.filter(application=app, user=request.user).exists()
    else:
        i_like = False

    if i_like:
        total_likes_count -= 1

    context = {
        "app": app,
        "svg": svg,
        "version": app_version,
        "i_like": i_like,
        "total_likes_count": total_likes_count,
        "last_updated": last_updated}
    return render(request, "detail.html", context=context)


@login_required
def toggle_like(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    like, created = Like.objects.get_or_create(user=request.user, application=application)
    if not created:
        like.delete()

    total_likes_count = application.like_set.count()
    i_like = Like.objects.filter(application=application, user=request.user).exists()

    if i_like:
        total_likes_count -= 1
    return JsonResponse({"total_likes_count": total_likes_count, "i_like": i_like})


def scientist(request, post_id):
    scientist = Scientist.objects.get(pk=post_id)

    context = {"staff": scientist, }
    return render(request, "developer.html", context=context)


def developer(request, post_id):
    developer = Developer.objects.get(pk=post_id)

    context = {"staff": developer, }
    return render(request, "developer.html", context=context)


def login(request):
    response = redirect('accounts/google/login/')
    return response


def get_last_updated(obj):
    content_type = ContentType.objects.get_for_model(obj)
    last_update = LogEntry.objects.filter(
        content_type=content_type,
        object_id=obj.pk,
        action_flag=2  # Action flag 2 corresponds to "CHANGE"
    ).order_by('-action_time').first()
    if last_update:
        return last_update.action_time.strftime('%m/%d/%Y')  # Format as mm/dd/yyyy
    return "N/A"


def fill_information(request):
    if request.method == 'POST':
        form = UserRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            other_explanation = form.cleaned_data.get('other_explanation', '')
            user = request.user
            # Fetch all users in the Approvers group
            approver_group = Group.objects.get(name='Approver')
            approvers = approver_group.user_set.all()

            # Construct the email content
            subject = 'SAMS New User Role Submission'
            message = f"""
                       
                       
                       User ID: <a href='https://sams.servirglobal.net/admin/auth/user/{user.id}/change/'>{user.id}</a>
                       Name: {user.get_full_name() or user.username}
                       Role: {role}
                       """
            if role == 'Other collaborator' and other_explanation:
                message += f"Other Explanation: {other_explanation}"

            # Send the email to all approvers
            approvers_emails = [approver.email for approver in approvers if approver.email]
            send_mail(subject, message, 'your_email@example.com', approvers_emails)

            # Redirect to home or another page after successful submission
            return redirect('home')
    else:
        form = UserRoleForm()

    return render(request, 'fill_information.html', {'form': form})


def about(request):
    return render(request, "about.html", context={})

def is_approver(user):
    return user.groups.filter(name='Approver').exists()

@login_required
@user_passes_test(is_approver)
def notifications(request):
    return render(request, "notifications.html", context={})


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
        new_log = Log.objects.create(application=application,
                                     log_entry=log_entry_text, user=request.user  # Assign the current user
                                     )

        # Return the new log entry as JSON response
        return JsonResponse(
            {'date': django_date_format(new_log.date_modified, "M. j, Y"),
             'log_entry': new_log.log_entry,
             'username': new_log.user.username})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def feedback_submit(request):
    if request.method == 'POST':
        feedback_entry_text = request.POST.get('feedback_entry')
        application_id = request.POST.get('application_id')

        application = get_object_or_404(Application, id=application_id)

        # Create a new feedback entry
        new_feedback = Feedback.objects.create(application=application,
                                               feedback_entry=feedback_entry_text, user=request.user
                                               # Assign the current user
                                               )

        # Return the new log entry as JSON response
        return JsonResponse(
            {'date': django_date_format(new_feedback.date_modified, "M. j, Y"),
             'feedback_entry': new_feedback.feedback_entry})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def general_feedback_submit(request):
    if request.method == 'POST':
        feedback_entry_text = request.POST.get('feedback')

        # Create a new feedback entry
        new_feedback = Feedback.objects.create(
            feedback_entry=feedback_entry_text, user=request.user  # Assign the current user
        )

        # Return the new log entry as JSON response
        return JsonResponse(
            {'date': django_date_format(new_feedback.date_modified, "M. j, Y"),
             'message': "Thank you for your feedback."})
    else:
        return JsonResponse({'error': 'Invalid request method'})
