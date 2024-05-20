# signals.py
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    # Check if the user is new
    print("handle this **********************")
    request.session['is_new_user'] = True
    print(reverse('fill_information'))  # Added for debugging
    return HttpResponseRedirect('fill_information')
