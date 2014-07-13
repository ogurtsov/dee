# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

import logging
logger = logging.getLogger(__name__)


def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        logger.info(user)
        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, _('Authentication failed'))
    return render(request, 'login-form.html', locals())


def dashboard(request):
    return render(request, 'dashboard.html', locals())
