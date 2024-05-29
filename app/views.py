from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import date as django_date_format

from .models import Application, Log, Feedback
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

app_version = 1.03


# Create your views here.
def index(request):
    is_new_user = request.session.get('is_new_user', False)
    if is_new_user:
        del request.session['is_new_user']
        return HttpResponseRedirect('fill_information')
    context = {"apps": Application.objects.exclude(shown=False).all().order_by("display_priority"),
        "service_areas": ServiceArea.objects.all(), "regions": Region.objects.all()}

    # Include new users if the request has new_users attribute (set by middleware)
    if hasattr(request, 'new_users'):
        context['new_users'] = request.new_users

    return render(request, "index.html", context=context)


def detail(request, post_id):
    app = Application.objects.get(pk=post_id)
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(app.url, image_factory=factory, box_size=10)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()

    context = {"app": app, "svg": svg, "version": app_version}
    return render(request, "detail.html", context=context)


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
            {'date': django_date_format(new_log.date_modified, "M. j, Y"), 'log_entry': new_log.log_entry})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def feedback_submit(request):
    if request.method == 'POST':
        feedback_entry_text = request.POST.get('feedback_entry')
        application_id = request.POST.get('application_id')

        application = get_object_or_404(Application, id=application_id)

        # Create a new feedback entry
        new_feedback = Feedback.objects.create(application=application,
            feedback_entry=feedback_entry_text, user=request.user  # Assign the current user
        )

        # Return the new log entry as JSON response
        return JsonResponse(
            {'date': django_date_format(new_feedback.date_modified, "M. j, Y"), 'feedback_entry': new_feedback.feedback_entry})
    else:
        return JsonResponse({'error': 'Invalid request method'})