# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout


def logout(request):
#    logout(request)
#    return redirect(reverse('home'))
    return HttpResponse('logout view')


def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    return render(request, 'login-form.html', locals())


def dashboard(request):
    return render(request, 'dashboard.html')
