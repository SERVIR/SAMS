# your_app/middleware/admin_banner.py
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta

from app.models import Feedback


class AdminBannerMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            seven_days_ago = timezone.now() - timedelta(days=7)

            # Define the groups to exclude
            excluded_groups = ["Approver", "scoscience", "Viewer"]

            # Retrieve the groups
            excluded_group_objects = Group.objects.filter(name__in=excluded_groups)

            # Get users who joined in the last 7 days
            new_users = User.objects.filter(date_joined__gte=seven_days_ago)

            # Exclude users who belong to any of the excluded groups
            new_users = new_users.exclude(groups__in=excluded_group_objects).distinct()
            unresolved_feedback = Feedback.objects.filter(resolved=False)

            if new_users or unresolved_feedback:

                if not hasattr(request, 'extras'):
                    request.extras = type('extras', (object,), {})()

                request.extras.new_users = new_users
                request.extras.unresolved_feedback = unresolved_feedback
        return None
