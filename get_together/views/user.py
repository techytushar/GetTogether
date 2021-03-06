from django.utils.translation import ugettext_lazy as _

from django.contrib import messages
from django.contrib.auth import logout as logout_user
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from events.models.profiles import Team, UserProfile, Member
from events.forms import UserForm, UserProfileForm

from events.models.events import Event, Place, Attendee

import datetime
import simplejson

from .teams import *
from .events import *

def edit_profile(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, message=_('You must be logged in to edit your profile.'))
        return redirect('login')

    user = request.user
    profile = request.user.profile

    if request.method == 'GET':
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'get_together/users/edit_profile.html', context)
    elif request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save()
            return redirect('home')
        else:
            context = {
            'user_form': user_form,
            'profile_form': profile_form,
            }
            return render(request, 'get_together/users/edit_profile.html', context)
    else:
     return redirect('home')

